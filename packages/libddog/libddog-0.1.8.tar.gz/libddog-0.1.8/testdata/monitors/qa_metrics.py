from typing import List

from libddog.metrics import Query, count_nonzero
from libddog.monitors import (
    Monitor,
    avg,
    change,
    last,
    max,
    metric_query,
    min,
    pct_change,
    sum,
)

CASES = [
    ("minimal metric query", metric_query(Query("aws.elb.requests").agg("sum"))),
    (
        "exhaustive metric query",
        metric_query(
            count_nonzero(
                Query("aws.elb.requests").agg("avg").by("az").fill("last", 45)
            ),
            pct_change(min(last("5m")), last("10m")),
        )
        < 43,
    ),
    (
        "metric query with minutely time aggregation",
        metric_query(Query("aws.elb.requests").agg("sum"), min(last("2m"))) > 2,
    ),
    (
        "metric query with hourly time aggregation",
        metric_query(Query("aws.elb.requests").agg("sum"), max(last("7h"))) >= 7,
    ),
    (
        "metric query with daily time aggregation",
        metric_query(Query("aws.elb.requests").agg("sum"), sum(last("1d"))) <= 50,
    ),
    (
        "metric query with weekly time aggregation",
        metric_query(
            Query("aws.elb.requests").agg("sum"), change(avg(last("1w")), last("1d"))
        )
        == 90,
    ),
]


def get_monitors() -> List[Monitor]:
    monitors = []

    for desc, query in CASES:
        monitor = Monitor(
            name=f"libddog QA: {desc}",
            message=f"Integration test case: {desc}",
            query=query,
            tags=["owner:libddog"],
        )
        monitor.tags.append(f"type:{monitor.type_desc.lower()}")
        monitors.append(monitor)

    return monitors
