from typing import List

from libddog.metrics import Query, count_nonzero
from libddog.monitors import (
    Monitor,
    MonitorOptions,
    MonitorThresholds,
    RenotifyStatus,
    last,
    metric_query,
    min,
    pct_change,
)


def get_monitors() -> List[Monitor]:
    query = (
        metric_query(
            count_nonzero(Query("aws.elb.requests").agg("avg").by("region").by("az")),
            pct_change(min(last("5m")), last("10m")),
        )
        > 43
    )

    monitor = Monitor(
        name=f"libddog QA: exhaustive monitor options",
        message=f"Integration test case: exhaustive monitor options",
        query=query,
        options=MonitorOptions(
            enable_logs_sample=True,
            escalation_message="this is the escalation message",
            evaluation_delay=901,
            groupby_simple_monitor=False,
            include_tags=True,
            new_group_delay=65,
            notify_audit=True,
            notify_no_data=False,
            renotify_interval=1200,
            renotify_occurrences=3,
            renotify_statuses=[RenotifyStatus.WARN, RenotifyStatus.NO_DATA],
            require_full_window=True,
            thresholds=MonitorThresholds(
                critical=43,
                critical_recovery=40,
                ok=10,
                warning=35,
                warning_recovery=30,
            ),
            timeout_h=2,
        ),
        priority=5,
        tags=["owner:libddog"],
    )

    return [monitor]
