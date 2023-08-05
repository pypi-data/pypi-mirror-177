import copy
import enum
import re
from typing import Any, Optional, Union

from libddog.metrics.bases import FormulaNode
from libddog.metrics.query import QueryMonad, QueryState, Rollup
from libddog.monitors.bases import AlertQuery
from libddog.monitors.exceptions import MetricAlertQueryValidationError


class TimeAggNode:
    def codegen(self) -> str:
        raise NotImplemented  # pragma: no cover


class last(TimeAggNode):
    rx_value = re.compile(r"((?P<mins>[0-9]+)m|(?P<hours>[0-9]+)h)|1d|1w")

    def __init__(self, period: str) -> None:
        match = self.rx_value.match(period)
        if match is None:
            raise MetricAlertQueryValidationError(f"last period invalid: {period!r}")

        mins_str = match.groupdict().get("mins")
        hours_str = match.groupdict().get("hours")

        if mins_str:
            mins = int(mins_str)
            if not 1 <= mins <= 10080:
                raise MetricAlertQueryValidationError(
                    f"last period out of range: {period!r}"
                )

        if hours_str:
            hours = int(hours_str)
            if not 1 <= hours <= 168:
                raise MetricAlertQueryValidationError(
                    f"last period out of range: {period!r}"
                )

        self.period = period

    def codegen(self) -> str:
        return f"last_{self.period}"


class TimeAggFunc(TimeAggNode):
    pass


class TimeAggFuncWithSingleNode(TimeAggFunc):
    def __init__(self, node: TimeAggNode) -> None:
        self.node = node

    def codegen(self) -> str:
        func_name = self.__class__.__name__
        return f"{func_name}({self.node.codegen()})"


class TimeAggFuncWithTwoNodes(TimeAggFunc):
    def __init__(self, left: TimeAggNode, right: TimeAggNode) -> None:
        self.left = left
        self.right = right

    def codegen(self) -> str:
        func_name = self.__class__.__name__
        return f"{func_name}({self.left.codegen()},{self.right.codegen()})"


class avg(TimeAggFuncWithSingleNode):
    pass


class change(TimeAggFuncWithTwoNodes):
    pass


class min(TimeAggFuncWithSingleNode):
    pass


class max(TimeAggFuncWithSingleNode):
    pass


class pct_change(TimeAggFuncWithTwoNodes):
    pass


class sum(TimeAggFuncWithSingleNode):
    pass


class Operator(enum.Enum):
    LT = "<"
    LE = "<="
    GT = ">"
    GE = ">="
    EQ = "=="
    NE = "!="

    def codegen(self) -> str:
        return self.value


class MetricAlertQueryState:
    """
    from: https://docs.datadoghq.com/api/latest/monitors/#create-a-monitor

    > Metric Alert Query

    > Example: time_aggr(time_window):space_aggr:metric{tags} [by {key}] operator #

    > - time_aggr: avg, sum, max, min, change, or pct_change
    > - time_window: last_#m (with # between 1 and 10080 depending on the
    monitor type) or last_#h(with # between 1 and 168 depending on the monitor
    type) or last_1d, or last_1w
    > - space_aggr: avg, sum, min, or max
    > - tags: one or more tags (comma-separated), or *
    > - key: a `key` in key:value tag syntax; defines a separate alert for each
    tag in the group (multi-alert)
    > - operator: <, <=, >, >=, ==, or !=
    > - #: an integer or decimal number used to set the threshold
    """

    def __init__(
        self,
        query: Union[QueryMonad, FormulaNode],
        time_agg: Optional[TimeAggFunc] = None,
        operator: Optional[Operator] = None,
        alert_threshold: Optional[float] = None,
    ) -> None:
        self.query = query
        self.time_agg = time_agg or avg(last("5m"))
        self.operator = operator or Operator.GE
        self.alert_threshold = alert_threshold if alert_threshold else 1

    def clone(self) -> "MetricAlertQueryState":
        return copy.deepcopy(self)

    def codegen(self) -> str:
        metric_query: Union[QueryMonad, QueryState, FormulaNode] = self.query

        if isinstance(self.query, QueryMonad):
            state = self.query._state.clone()

            # Remove rollup function because time aggregation works differently
            # for metric alert queries.
            state.funcs = [func for func in state.funcs if not isinstance(func, Rollup)]

            metric_query = state

        # NOTE: If it's a FormulaNode removing the rollup function would require
        # recursing into all nested functions. Technically this should also be
        # done here, but the workaround is just not to use .rollup() in the
        # input.

        query = "%s:%s %s %s" % (
            self.time_agg.codegen(),
            metric_query.codegen(),
            self.operator.codegen(),
            self.alert_threshold,
        )

        return query


class MetricAlertQueryMonad(AlertQuery):
    def __init__(self, state: MetricAlertQueryState) -> None:
        self._state = state

    def __gt__(self, value: float) -> "MetricAlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.GT
        state.alert_threshold = value
        return self.__class__(state)

    def __ge__(self, value: float) -> "MetricAlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.GE
        state.alert_threshold = value
        return self.__class__(state)

    def __lt__(self, value: float) -> "MetricAlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.LT
        state.alert_threshold = value
        return self.__class__(state)

    def __le__(self, value: float) -> "MetricAlertQueryMonad":
        state = self._state.clone()

        state.operator = Operator.LE
        state.alert_threshold = value
        return self.__class__(state)

    def __eq__(self, value: float) -> "MetricAlertQueryMonad":  # type: ignore
        state = self._state.clone()

        state.operator = Operator.EQ
        state.alert_threshold = value
        return self.__class__(state)

    def __ne__(self, value: float) -> "MetricAlertQueryMonad":  # type: ignore
        state = self._state.clone()

        state.operator = Operator.NE
        state.alert_threshold = value
        return self.__class__(state)

    def codegen(self) -> str:
        return self._state.codegen()


def metric_query(
    query: Union[QueryMonad, FormulaNode], time_agg: Optional[TimeAggFunc] = None
) -> MetricAlertQueryMonad:
    state = MetricAlertQueryState(query=query, time_agg=time_agg)
    return MetricAlertQueryMonad(state)
