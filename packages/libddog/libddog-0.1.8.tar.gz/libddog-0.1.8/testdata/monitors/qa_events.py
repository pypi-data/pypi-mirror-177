from typing import List

from libddog.monitors import Monitor, event_query

CASES = [
    ("minimal event query", event_query("status:error")),
    (
        "exhaustive event query",
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region", "service")
        .last("1h")
        < 1,
    ),
    (
        "event query without rollup",
        event_query("status:warn *SIGILL*").by("region", "service").last("1h") > 1,
    ),
    (
        "event query with rollup without measure",
        event_query("status:warn *SIGILL*")
        .rollup("count")
        .by("region", "service")
        .last("1h")
        == 1,
    ),
    (
        "event query without by",
        event_query("status:warn *SIGILL*").rollup("avg", "host").last("1h") != 1,
    ),
    (
        "event query with chained by",
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region")
        .by("service")
        .last("1h")
        <= 1,
    ),
    (
        "event query without last",
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region", "service")
        >= 1,
    ),
    (
        "event query without operator nor threshold",
        event_query("status:warn *SIGILL*")
        .rollup("avg", "host")
        .by("region", "service")
        .last("1h"),
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
