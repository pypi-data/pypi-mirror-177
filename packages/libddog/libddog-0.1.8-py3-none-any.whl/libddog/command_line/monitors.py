import fnmatch
import os
from typing import List

from libddog.command_line.console import ConsoleWriter
from libddog.crud.errors import AbstractCrudError
from libddog.crud.monitors import MonitorManager
from libddog.monitors.monitors import Monitor
from libddog.tools.timekeeping import parse_date, time_since, utcnow


class MonitorManagerCli:
    def __init__(self, proj_path: str) -> None:
        self.proj_path = os.path.abspath(proj_path)

        self.writer = ConsoleWriter()
        self.manager = MonitorManager(self.proj_path)

    def filter_definitions(
        self, pattern: str, monitors: List[Monitor]
    ) -> List[Monitor]:
        return [mon for mon in monitors if fnmatch.fnmatch(mon.name, pattern)]

    def delete_live(self, *, id: int) -> int:
        # Take a snapshot first to make restoring it possible
        exit_code = self.snapshot_live(id=id)
        if exit_code != os.EX_OK:
            return exit_code

        self.writer.print("Deleting live monitor with id: %r... ", id)

        try:
            self.manager.delete_monitor(id=id)
            self.writer.println("done")

        except AbstractCrudError as exc:
            self.writer.report_failed(exc)
            return os.EX_UNAVAILABLE

        return os.EX_OK

    def list_defs(self) -> int:
        monitors = None

        try:
            monitors = self.manager.load_definitions()

        except AbstractCrudError as exc:
            self.writer.report_failed(exc)
            return os.EX_UNAVAILABLE

        def format_tags(monitor: Monitor) -> str:
            return ",".join(monitor.tags)

        # sort by name
        monitors = sorted(monitors, key=lambda mon: mon.name.lower())

        tags_width = 4
        if monitors:
            tags_width = max([len(format_tags(mon)) for mon in monitors])

        fmt = "%-6s  %-" + str(tags_width) + "s  %s"
        self.writer.println(fmt, "TYPE", "TAGS", "NAME")

        for monitor in monitors:
            self.writer.println(
                fmt,
                monitor.type_desc,
                format_tags(monitor),
                monitor.name,
            )

        return os.EX_OK

    def list_live(self) -> int:
        monitor_dcts = None

        try:
            monitor_dcts = self.manager.list_monitors()

        except AbstractCrudError as exc:
            self.writer.report_failed(exc)
            return os.EX_UNAVAILABLE

        fmt = "%11s  %24s  %4s  %7s  %s"
        header_cols = (
            "ID",
            "USER",
            "TIME",
            "LIBDDOG",
            "NAME",
        )
        self.writer.println(fmt, *header_cols)

        tuples = []
        for dct in monitor_dcts:
            modified_at = parse_date(dct["modified"])
            modified_ago = utcnow() - modified_at
            tuples.append((modified_ago, dct))

        # sort by oldest modified time first
        tuples.sort(reverse=True)

        for modified_ago, dct in tuples:
            id = dct["id"]
            message = dct["message"]
            user_handle = dct["creator"]["email"]
            user_symbol = "c"
            libddog_maintained = "n"
            name = dct["name"]

            # user@company.com -> user
            user_handle = user_handle.split("@")[0]
            user_handle = f"{user_handle} [{user_symbol}]"

            # detect our own fingerprint in the message
            if self.manager._libddog_proj_name in message:
                libddog_maintained = "y"

            cols = (
                id,
                user_handle,
                time_since(modified_ago),
                libddog_maintained,
                name,
            )
            self.writer.println(fmt, *cols)

        self.writer.println("%d monitors found" % len(tuples))

        return os.EX_OK

    def publish_draft(self, *, name_pat: str) -> int:
        monitors = self.manager.load_definitions()
        monitors = self.filter_definitions(name_pat, monitors)

        if not monitors:
            self.writer.println("Name pattern %r did not match any monitors", name_pat)
            return os.EX_USAGE

        if len(monitors) > 1:
            fmt = "\n".join([f"- {mon.name}" for mon in monitors])
            self.writer.println(
                "Name pattern %r matched multiple monitors:\n%s", name_pat, fmt
            )
            return os.EX_USAGE

        monitor = monitors[0]
        monitor.name = self.manager.get_draft_name(monitor)
        existing = self.manager.find_first_monitor_with_name(monitor.name)

        if existing:
            id = int(existing["id"])

            self.writer.print(
                f"Updating monitor with id: {id!r} named: {monitor.name!r}... "
            )
            try:
                self.manager.update_monitor(monitor=monitor, id=id)
                self.writer.println("done")

            except AbstractCrudError as exc:
                self.writer.report_failed(exc)
                return os.EX_IOERR

        else:
            self.writer.print(f"Creating monitor named: {monitor.name!r}... ")
            try:
                id = self.manager.create_monitor(monitor=monitor)
                self.writer.println("created with id: %r", id)

            except AbstractCrudError as exc:
                self.writer.report_failed(exc)
                return os.EX_IOERR

        return os.EX_OK

    def publish_live(self, *, name_pat: str) -> int:
        monitors = self.manager.load_definitions()
        monitors = self.filter_definitions(name_pat, monitors)

        for monitor in monitors:
            existing = self.manager.find_first_monitor_with_name(monitor.name)

            if existing:
                id = int(existing["id"])

                # Take a snapshot first to make restoring it possible
                exit_code = self.snapshot_live(id=id)
                if exit_code != os.EX_OK:
                    return exit_code

                self.writer.print(
                    f"Updating monitor with id: {id!r} named: {monitor.name!r}... "
                )

                try:
                    self.manager.update_monitor(monitor=monitor, id=id)
                    self.writer.println("done")

                except AbstractCrudError as exc:
                    self.writer.report_failed(exc)
                    return os.EX_IOERR

            else:
                self.writer.print(f"Creating monitor named: {monitor.name!r}... ")

                try:
                    id = self.manager.create_monitor(monitor=monitor)
                    self.writer.println("created with id: %r", id)

                except AbstractCrudError as exc:
                    self.writer.report_failed(exc)
                    return os.EX_IOERR

        return os.EX_OK

    def snapshot_live(self, *, id: int) -> int:
        self.writer.print("Creating snapshot of live monitor with id: %r... ", id)

        try:
            fp = self.manager.create_snapshot(id)
            self.writer.println("saved to: %s", fp)

        except AbstractCrudError as exc:
            self.writer.report_failed(exc)
            return os.EX_UNAVAILABLE

        return os.EX_OK
