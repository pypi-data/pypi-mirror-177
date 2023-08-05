from libddog.metrics import Query, count_nonzero
from libddog.monitors import (
    Monitor,
    MonitorOptions,
    MonitorThresholds,
    RenotifyStatus,
    event_query,
    last,
    metric_query,
    min,
    pct_change,
)


def test__minimal() -> None:
    monitor = Monitor(
        name="minimal monitor options",
        message="minimal monitor options",
        query=event_query("*error*"),
    )

    assert monitor.as_dict() == {
        "id": None,
        "message": "minimal monitor options",
        "name": "minimal monitor options",
        "options": {
            "enable_logs_sample": None,
            "escalation_message": None,
            "evaluation_delay": None,
            "groupby_simple_monitor": False,
            "include_tags": True,
            "new_group_delay": None,
            "no_data_timeframe": None,
            "notify_audit": False,
            "notify_no_data": False,
            "renotify_interval": None,
            "renotify_occurrences": None,
            "renotify_statuses": None,
            "require_full_window": False,
            "threshold_windows": None,
            "thresholds": None,
            "timeout_h": None,
        },
        "priority": None,
        "query": 'events("*error*").rollup("count").last("5m") >= 1',
        "restricted_roles": None,
        "tags": [],
        "type": "event-v2 alert",
    }


def test__exhaustive() -> None:
    query = (
        metric_query(
            count_nonzero(Query("aws.elb.requests").agg("avg").by("region").by("az")),
            pct_change(min(last("5m")), last("10m")),
        )
        > 43
    )

    monitor = Monitor(
        name="exhaustive monitor options",
        message="exhaustive monitor options",
        query=query,
        options=MonitorOptions(
            enable_logs_sample=True,
            escalation_message="this is the escalation message",
            evaluation_delay=901,
            groupby_simple_monitor=False,
            include_tags=True,
            new_group_delay=65,
            no_data_timeframe=10,
            notify_audit=True,
            notify_no_data=False,
            renotify_interval=1200,
            renotify_occurrences=3,
            renotify_statuses=[RenotifyStatus.WARN],
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

    assert monitor.as_dict() == {
        "id": None,
        "message": "exhaustive monitor options",
        "name": "exhaustive monitor options",
        "options": {
            "enable_logs_sample": True,
            "escalation_message": "this is the escalation message",
            "evaluation_delay": 901,
            "groupby_simple_monitor": False,
            "include_tags": True,
            "new_group_delay": 65,
            "no_data_timeframe": 10,
            "notify_audit": True,
            "notify_no_data": False,
            "renotify_interval": 1200,
            "renotify_occurrences": 3,
            "renotify_statuses": ["warn"],
            "require_full_window": True,
            "threshold_windows": None,
            "thresholds": {
                "critical": 43,
                "critical_recovery": 40,
                "ok": 10,
                "warning": 35,
                "warning_recovery": 30,
            },
            "timeout_h": 2,
        },
        "priority": 5,
        "query": "pct_change(min(last_5m),last_10m):count_nonzero(avg:aws.elb.requests{*} "
        "by {region, az}) > 43",
        "restricted_roles": None,
        "tags": ["owner:libddog"],
        "type": "query alert",
    }
