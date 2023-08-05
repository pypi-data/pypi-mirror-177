import pytest

from libddog.monitors import event_query
from libddog.monitors.exceptions import EventV2AlertQueryValidationError

# 'empty' and 'full' states


def test__minimal() -> None:
    query = event_query("*error*")

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("5m") >= 1'
    )


def test__exhaustive() -> None:
    query = (
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region", "service")
        .last("1h")
        != 1
    )

    assert query._state.codegen() == (
        'events("status:warn *SIGILL*").rollup("avg","host")'
        '.by("region,service").last("1h") != 1'
    )


# start with the 'full' state and remove parts, covering most combinations


def test__exhaustive__no_rollup() -> None:
    query = event_query("status:warn *SIGILL*").by("region", "service").last("1h") != 1

    assert query._state.codegen() == (
        'events("status:warn *SIGILL*").rollup("count")'
        '.by("region,service").last("1h") != 1'
    )


def test__exhaustive__rollup_without_measure() -> None:
    query = (
        event_query("status:warn *SIGILL*")
        .rollup("count")
        .by("region", "service")
        .last("1h")
        != 1
    )

    assert query._state.codegen() == (
        'events("status:warn *SIGILL*").rollup("count")'
        '.by("region,service").last("1h") != 1'
    )


def test__exhaustive__no_by() -> None:
    query = event_query("status:warn *SIGILL*").rollup("avg", "host").last("1h") != 1

    assert query._state.codegen() == (
        'events("status:warn *SIGILL*").rollup("avg","host").last("1h") != 1'
    )


def test__exhaustive__chained_by() -> None:
    query = (
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region")
        .by("service")
        .last("1h")
        != 1
    )

    assert query._state.codegen() == (
        'events("status:warn *SIGILL*").rollup("avg","host")'
        '.by("region,service").last("1h") != 1'
    )


def test__exhaustive__no_last() -> None:
    query = (
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region", "service")
        != 1
    )

    assert query._state.codegen() == (
        'events("status:warn *SIGILL*").rollup("avg","host")'
        '.by("region,service").last("5m") != 1'
    )


def test__exhaustive__no_operator_nor_threshold() -> None:
    query = (
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region", "service")
        .last("1h")
    )

    assert query._state.codegen() == (
        'events("status:warn *SIGILL*").rollup("avg","host")'
        '.by("region,service").last("1h") >= 1'
    )


# rollup


def test__rollup_invalid_method() -> None:
    with pytest.raises(EventV2AlertQueryValidationError) as ctx:
        event_query("*error*").rollup("flat")

    assert ctx.value.args[0] == (
        "Rollup method 'flat' must be one of 'avg', 'cardinality', 'count'"
    )


# by


def test__by_invalid_tag_name() -> None:
    with pytest.raises(EventV2AlertQueryValidationError) as ctx:
        event_query("*error*").by("aws region")

    assert ctx.value.args[0] == "Invalid by tag name: 'aws region'"


# last


def test__last__invalid_input() -> None:
    with pytest.raises(EventV2AlertQueryValidationError) as ctx:
        event_query("*error*").last("1y")

    assert ctx.value.args[0] == "last period invalid: '1y'"


def test__last_minutes() -> None:
    query = event_query("*error*").last("2m")

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("2m") >= 1'
    )


def test__last_minutes_out_of_range() -> None:
    with pytest.raises(EventV2AlertQueryValidationError) as ctx:
        event_query("*error*").last("0m")

    assert ctx.value.args[0] == "last period out of range: '0m'"


def test__last_hours() -> None:
    query = event_query("*error*").last("10h")

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("10h") >= 1'
    )


def test__last_hours_out_of_range() -> None:
    with pytest.raises(EventV2AlertQueryValidationError) as ctx:
        event_query("*error*").last("49h")

    assert ctx.value.args[0] == "last period out of range: '49h'"


# operator


def test__operator_invalid() -> None:
    with pytest.raises(TypeError):
        event_query("*error*") << 1  # type: ignore


def test__operator_lt() -> None:
    query = event_query("*error*") < 7

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("5m") < 7'
    )


def test__operator_le() -> None:
    query = event_query("*error*") <= 2

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("5m") <= 2'
    )


def test__operator_gt() -> None:
    query = event_query("*error*") > 19

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("5m") > 19'
    )


def test__operator_ge() -> None:
    query = event_query("*error*") >= 2.3

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("5m") >= 2.3'
    )


def test__operator_eq() -> None:
    query = event_query("*error*") == -4

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("5m") == -4'
    )


def test__operator_ne() -> None:
    query = event_query("*error*") != 0

    assert query._state.codegen() == (
        'events("*error*").rollup("count").last("5m") != 0'
    )
