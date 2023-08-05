import pytest

from libddog.metrics import Query, count_nonzero
from libddog.monitors import avg, change, last, max, metric_query, min, pct_change, sum
from libddog.monitors.exceptions import MetricAlertQueryValidationError

# 'empty' and 'full' states


def test__minimal() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum"))

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} >= 1"


def test__exhaustive() -> None:
    query = (
        metric_query(
            count_nonzero(
                Query("aws.elb.requests").agg("avg").by("az").fill("last", 45)
            ),
            pct_change(min(last("5m")), last("10m")),
        )
        < 43
    )

    assert query._state.codegen() == (
        "pct_change(min(last_5m),last_10m):"
        "count_nonzero(avg:aws.elb.requests{*} by {az}.fill(last, 45)) < 43"
    )


# rollup removal


def test__rollup__remove() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum").rollup("avg"))

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} >= 1"


# time_agg


def test__time_agg__invalid_input() -> None:
    with pytest.raises(MetricAlertQueryValidationError) as ctx:
        metric_query(Query("aws.elb.requests").agg("sum"), avg(last("7 seconds away")))

    assert ctx.value.args[0] == "last period invalid: '7 seconds away'"


def test__time_agg__minutes() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum"), avg(last("2m")))

    assert query._state.codegen() == "avg(last_2m):sum:aws.elb.requests{*} >= 1"


def test__time_agg__minutes_out_of_range() -> None:
    with pytest.raises(MetricAlertQueryValidationError) as ctx:
        metric_query(Query("aws.elb.requests").agg("sum"), avg(last("10081m")))

    assert ctx.value.args[0] == "last period out of range: '10081m'"


def test__time_agg__hours() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum"), min(last("7h")))

    assert query._state.codegen() == "min(last_7h):sum:aws.elb.requests{*} >= 1"


def test__time_agg__hours_out_of_range() -> None:
    with pytest.raises(MetricAlertQueryValidationError) as ctx:
        metric_query(Query("aws.elb.requests").agg("sum"), avg(last("169h")))

    assert ctx.value.args[0] == "last period out of range: '169h'"


def test__time_agg__days() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum"), max(last("1d")))

    assert query._state.codegen() == "max(last_1d):sum:aws.elb.requests{*} >= 1"


def test__time_agg__days_out_of_range() -> None:
    with pytest.raises(MetricAlertQueryValidationError) as ctx:
        metric_query(Query("aws.elb.requests").agg("sum"), avg(last("2d")))

    assert ctx.value.args[0] == "last period invalid: '2d'"


def test__time_agg__weeks() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum"), sum(last("1w")))

    assert query._state.codegen() == "sum(last_1w):sum:aws.elb.requests{*} >= 1"


def test__time_agg__weeks_out_of_range() -> None:
    with pytest.raises(MetricAlertQueryValidationError) as ctx:
        metric_query(Query("aws.elb.requests").agg("sum"), avg(last("2w")))

    assert ctx.value.args[0] == "last period invalid: '2w'"


def test__time_agg__change() -> None:
    query = metric_query(
        Query("aws.elb.requests").agg("sum"), change(avg(last("20m")), last("4m"))
    )

    assert query._state.codegen() == (
        "change(avg(last_20m),last_4m):sum:aws.elb.requests{*} >= 1"
    )


# operator


def test__operator_invalid() -> None:
    with pytest.raises(TypeError):
        metric_query(Query("aws.elb.requests").agg("sum")) << 1  # type: ignore


def test__operator_lt() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum")) < 7

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} < 7"


def test__operator_le() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum")) <= 2

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} <= 2"


def test__operator_gt() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum")) > 17

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} > 17"


def test__operator_ge() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum")) >= 4.13

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} >= 4.13"


def test__operator_eq() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum")) == -2

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} == -2"


def test__operator_ne() -> None:
    query = metric_query(Query("aws.elb.requests").agg("sum")) != -1

    assert query._state.codegen() == "avg(last_5m):sum:aws.elb.requests{*} != -1"
