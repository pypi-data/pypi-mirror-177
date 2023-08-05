import copy
import enum
import re
from typing import List, Optional, Type

from libddog.monitors.bases import AlertQuery
from libddog.monitors.exceptions import EventV2AlertQueryValidationError
from libddog.parsing.query_parser import QueryParser


def reverse_enum(enum_cls: Type[enum.Enum], literal: str, label: str) -> enum.Enum:
    alternatives: List[enum.Enum] = list(enum_cls)
    for alternative in alternatives:
        if literal == alternative.value:
            return alternative

    values = [alt.value for alt in alternatives if alt.value]
    values_fmt = ", ".join([f"{alt!r}" for alt in sorted(values)])
    raise EventV2AlertQueryValidationError(
        "%s %r must be one of %s" % (label, literal, values_fmt)
    )


class LogQuery:
    """
    Contains a log query in the form of a text string as detailed at:
    https://docs.datadoghq.com/logs/explorer/search_syntax/

    Example:
      sources:nagios status:error,warning priority:normal tags:"string query"

    The query is not checked for correctness.
    """

    def __init__(self, *, query: str) -> None:
        self.query = query

    def codegen(self) -> str:
        return self.query


class RollupMethod(enum.Enum):
    AVG = "avg"
    CARDINALITY = "cardinality"
    COUNT = "count"

    def codegen(self) -> str:
        return self.value


class Rollup:
    def __init__(self, *, method: RollupMethod, measure: Optional[str] = None) -> None:
        self.method = method
        self.measure = measure

    def codegen(self) -> str:
        measure = f',"{self.measure}"' if self.measure else ""
        return f'.rollup("{self.method.codegen()}"{measure})'


class Last:
    rx_value = re.compile(r"(?P<num>[0-9]+)(?P<unit>m|h)")

    def __init__(self, num: int, unit: str) -> None:
        self.num = num
        self.unit = unit

    @classmethod
    def from_str(cls, period: str) -> "Last":
        match = cls.rx_value.match(period)
        if match is None:
            raise EventV2AlertQueryValidationError(f"last period invalid: {period!r}")

        num = int(match.group("num"))
        unit = match.group("unit")

        if unit == "m" and not 1 <= num <= 2880:
            raise EventV2AlertQueryValidationError(
                f"last period out of range: {period!r}"
            )
        if unit == "h" and not 1 <= num <= 48:
            raise EventV2AlertQueryValidationError(
                f"last period out of range: {period!r}"
            )

        return cls(num=num, unit=unit)

    def codegen(self) -> str:
        return f'.last("{self.num}{self.unit}")'


class Operator(enum.Enum):
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    EQ = "=="
    NE = "!="

    def codegen(self) -> str:
        return self.value


class EventV2AlertQueryState:
    """
    from: https://docs.datadoghq.com/api/latest/monitors/#create-a-monitor

    > Event V2 Alert Query

    > Example: events(query).rollup(rollup_method[, measure]).last(time_window) operator #

    > - query: The search query - following the Log search syntax.
    > - rollup_method: The stats roll-up method - supports count, avg and
    cardinality.
    > - measure: For avg and cardinality rollup_method - specify the measure or
    the facet name you want to use.
    > - time_window: #m (between 1 and 2880), #h (between 1 and 48).
    > - operator: <, <=, >, >=, ==, or !=.
    > - #: an integer or decimal number used to set the threshold.
    """

    def __init__(
        self,
        *,
        query: LogQuery,
        rollup: Optional[Rollup] = None,
        by: Optional[List[str]] = None,
        last: Optional[Last] = None,
        operator: Optional[Operator] = None,
        alert_threshold: Optional[float] = None,
    ) -> None:
        self.query = query
        self.rollup = rollup or Rollup(method=RollupMethod.COUNT)
        self.by = by or []
        self.last = last or Last(num=5, unit="m")
        self.operator = operator or Operator.GE
        self.alert_threshold = alert_threshold if alert_threshold is not None else 1

    def clone(self) -> "EventV2AlertQueryState":
        return copy.deepcopy(self)

    def codegen(self) -> str:
        by = ""
        if self.by:
            items = ",".join(self.by)
            by = f'.by("{items}")'

        query = 'events("%s")%s%s%s %s %s' % (
            self.query.codegen(),
            self.rollup.codegen(),
            by,
            self.last.codegen(),
            self.operator.codegen(),
            self.alert_threshold,
        )

        return query


class EventV2AlertQueryMonad(AlertQuery):
    def __init__(self, state: EventV2AlertQueryState) -> None:
        self._state = state

    def rollup(
        self, method: str, measure: Optional[str] = None
    ) -> "EventV2AlertQueryMonad":
        state = self._state.clone()

        variant = reverse_enum(RollupMethod, method, label="Rollup method")
        assert isinstance(variant, RollupMethod)  # help mypy
        rollup = Rollup(method=variant, measure=measure)

        state.rollup = rollup
        return self.__class__(state)

    def by(self, *tags: str) -> "EventV2AlertQueryMonad":
        state = self._state.clone()
        by_tags: List[str] = state.by or []

        parser = QueryParser.get_instance()

        for tag in tags:
            if not parser.is_valid_tag_name(tag):
                raise EventV2AlertQueryValidationError("Invalid by tag name: %r" % tag)

            if tag not in by_tags:
                by_tags.append(tag)

        state.by = by_tags
        return self.__class__(state)

    def last(self, period: str) -> "EventV2AlertQueryMonad":
        state = self._state.clone()

        last = Last.from_str(period)

        state.last = last
        return self.__class__(state)

    def __gt__(self, value: float) -> "EventV2AlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.GT
        state.alert_threshold = value
        return self.__class__(state)

    def __ge__(self, value: float) -> "EventV2AlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.GE
        state.alert_threshold = value
        return self.__class__(state)

    def __lt__(self, value: float) -> "EventV2AlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.LT
        state.alert_threshold = value
        return self.__class__(state)

    def __le__(self, value: float) -> "EventV2AlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.LE
        state.alert_threshold = value
        return self.__class__(state)

    def __eq__(self, value: float) -> "EventV2AlertQueryMonad":  # type: ignore
        state = self._state.clone()

        state.operator = Operator.EQ
        state.alert_threshold = value
        return self.__class__(state)

    def __ne__(self, value: float) -> "EventV2AlertQueryMonad":  # type: ignore
        state = self._state.clone()

        state.operator = Operator.NE
        state.alert_threshold = value
        return self.__class__(state)

    def codegen(self) -> str:
        return self._state.codegen()


def event_query(query: str) -> EventV2AlertQueryMonad:
    state = EventV2AlertQueryState(query=LogQuery(query=query))
    return EventV2AlertQueryMonad(state)
