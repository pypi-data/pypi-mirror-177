from typing import List

from libddog.monitors.event_v2_alert_query import EventV2AlertQueryMonad
from libddog.monitors.metric_alert_query import MetricAlertQueryMonad
from libtests.managers import QAMonitorManager
from libtests.matchers import PatchInstruction, assign, obj_matcher

PATCHES: List[PatchInstruction] = [
    assign('.["created"]', "created"),
    assign('.["created_at"]', "created-at"),
    assign('.["creator"]', "creator"),
    assign('.["deleted"]', "deleted"),
    assign('.["id"]', "id"),
    assign('.["modified"]', "modified"),
    assign('.["multi"]', "multi"),
    assign('.["options"]["new_host_delay"]', "new_host_delay"),
    assign('.["options"]["silenced"]', "silenced"),
    assign('.["options"]["thresholds"]', "thresholds"),
    assign('.["org_id"]', "org_id"),
    assign('.["overall_state"]', "overall_state"),
    assign('.["overall_state_modified"]', "overall_state_modified"),
]


def test_put_and_get_event_monitors() -> None:
    mgr = QAMonitorManager()
    monitors = mgr.load_definition_by_query_class(cls=EventV2AlertQueryMonad)

    for monitor in monitors:
        monitor_id = mgr.assign_id_to_monitor(monitor)

        # put the monitor
        mgr.update_live_monitor(monitor, monitor_id)

        # now read it back and assert that it matches our model
        expected = monitor.as_dict()
        actual = mgr.manager.get_monitor(id=monitor_id)

        assert obj_matcher(expected, PATCHES) == obj_matcher(
            actual, PATCHES
        ), f"failed on: {monitor.name!r}"


def test_put_and_get_metric_monitors() -> None:
    mgr = QAMonitorManager()
    monitors = mgr.load_definition_by_query_class(cls=MetricAlertQueryMonad)

    for monitor in monitors:
        monitor_id = mgr.assign_id_to_monitor(monitor)

        # put the monitor
        mgr.update_live_monitor(monitor, monitor_id)

        # now read it back and assert that it matches our model
        expected = monitor.as_dict()
        actual = mgr.manager.get_monitor(id=monitor_id)

        assert obj_matcher(expected, PATCHES) == obj_matcher(
            actual, PATCHES
        ), f"failed on: {monitor.name!r}"


def test_monitor_lifecycle() -> None:
    mgr = QAMonitorManager()
    monitors = mgr.load_definition_by_query_class(cls=EventV2AlertQueryMonad)
    monitor = monitors[0]

    payload = mgr.manager.find_first_monitor_with_name(monitor.name)
    if payload:
        monitor_id = payload["id"]
        mgr.manager.delete_monitor(id=monitor_id)

    monitor_id = mgr.manager.create_monitor(monitor)
    mgr.manager.get_monitor(id=monitor_id)
    mgr.manager.update_monitor(monitor, id=monitor_id)
    mgr.manager.delete_monitor(id=monitor_id)
