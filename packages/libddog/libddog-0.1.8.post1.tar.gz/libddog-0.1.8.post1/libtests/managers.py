import re
from datetime import datetime
from pathlib import Path
from typing import List, Type

from libddog.crud.dashboards import DashboardManager
from libddog.crud.monitors import MonitorManager
from libddog.dashboards import Dashboard
from libddog.monitors import Monitor
from libddog.monitors.bases import AlertQuery


class QADashboardManager:
    # detect occurrences of:  %(variable)s
    rx_string_template = re.compile("%\\([a-zA-Z0-9_]+\\)s")

    def __init__(self) -> None:
        proj_root = Path(__file__).parent.parent
        testdata_dir = proj_root.joinpath("testdata").absolute()

        self.manager = DashboardManager(proj_path=str(testdata_dir))

    def load_definition_by_title(self, title: str) -> Dashboard:
        dashboards = self.manager.load_definitions()
        for dashboard in dashboards:
            if dashboard.title == title:
                return dashboard

        raise RuntimeError("Failed to get dashboard with title: %s" % title)

    def assign_id_to_dashboard(self, dashboard: Dashboard) -> str:
        all_dashboards = self.manager.list_dashboards()

        existing_id: str = ""
        for dash in all_dashboards:
            if dash["title"] == dashboard.title:
                existing_id = dash["id"]
                return existing_id

        return self.manager.create_dashboard(dashboard=dashboard)

    def update_live_dashboard(self, dashboard: Dashboard, id: str) -> None:
        if self.rx_string_template.search(dashboard.desc):
            raise RuntimeError(
                "Dashboard desc contains unpopulated template: %s" % dashboard.desc
            )

        self.manager.update_dashboard(dashboard, id)


class QAMonitorManager:
    # detect occurrences of:  %(variable)s
    rx_string_template = re.compile("%\\([a-zA-Z0-9_]+\\)s")

    def __init__(self) -> None:
        proj_root = Path(__file__).parent.parent
        testdata_dir = proj_root.joinpath("testdata").absolute()

        self.manager = MonitorManager(proj_path=str(testdata_dir))

    def load_definition_by_query_class(self, cls: Type[AlertQuery]) -> List[Monitor]:
        monitors = []

        all_monitors = self.manager.load_definitions()
        for monitor in all_monitors:
            if isinstance(monitor.query, cls):
                monitors.append(monitor)

        return monitors

    def assign_id_to_monitor(self, monitor: Monitor) -> int:
        all_monitors = self.manager.list_monitors()

        existing_id: int = -1
        for mon in all_monitors:
            if mon["name"] == monitor.name:
                existing_id = mon["id"]
                return existing_id

        return self.manager.create_monitor(monitor=monitor)

    def update_live_monitor(self, monitor: Monitor, id: int) -> None:
        if self.rx_string_template.search(monitor.message):
            raise RuntimeError(
                "Monitor message contains unpopulated template: %s" % monitor.message
            )

        self.manager.update_monitor(monitor, id)
