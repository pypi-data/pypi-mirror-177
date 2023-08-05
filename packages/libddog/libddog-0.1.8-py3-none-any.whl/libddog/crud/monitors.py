import importlib
import json
import os
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import List, Optional

import libddog
from libddog.common.types import JsonDict
from libddog.crud.client import DatadogClient
from libddog.crud.errors import (
    MonitorDefinitionsImportError,
    MonitorDefinitionsLoadError,
)
from libddog.monitors.monitors import Monitor
from libddog.tools.git import GitHelper
from libddog.tools.text import sanitize_title_for_filename
from libddog.tools.timekeeping import format_datetime_for_filename, utcnow


class MonitorManager:
    _name_sentinel = "Untitled monitor"
    _snapshot_dirname = "_snapshots_monitors"

    _defs_containing_dir = "config"
    _defs_module_name = "monitors"
    _defs_import_path = f"{_defs_containing_dir}.{_defs_module_name}"

    _libddog_proj_name = "libddog"
    _libddog_proj_url = "https://github.com/nearmap/libddog"

    def __init__(self, proj_path: str) -> None:
        self.proj_path = proj_path
        self.snapshots_path: Path = Path(self.proj_path) / Path(self._snapshot_dirname)
        self.git = GitHelper()

        self._client: Optional[DatadogClient] = None  # lazy attribute

    @property
    def client(self) -> DatadogClient:
        if self._client is None:
            self._client = DatadogClient()
            self._client.load_credentials_from_environment()

        return self._client

    def load_definitions_module(self) -> ModuleType:
        # add proj_path to sys.path to make 'config' importable
        if self.proj_path not in sys.path:
            sys.path.append(self.proj_path)

        import_path = self._defs_import_path
        load_func = "get_monitors"

        # import the module
        try:
            monitors_module = importlib.import_module(import_path)
        except ModuleNotFoundError as exc:
            error = (
                f"Failed to import definitions module "
                f"{import_path!r}: {exc.args[0]}"
            )
            raise MonitorDefinitionsImportError(errors=[error])

        # probe for get_monitors()
        get_monitors = getattr(monitors_module, load_func, None)
        if get_monitors is None or not callable(get_monitors):
            error = (
                f"Definitions module {self._defs_import_path!r} "
                f"does not contain {load_func!r} function"
            )
            raise MonitorDefinitionsLoadError(errors=[error])

        # try calling get_monitors
        monitors = get_monitors()

        errors = []
        if not isinstance(monitors, list):
            error = f"{load_func!r} did not return a list of Monitor instances"
            errors.append(error)

        if not errors:
            for idx, monitor in enumerate(monitors):
                if not isinstance(monitor, Monitor):
                    error = f"{idx}th value returned was not a Monitor: {monitor!r}"
                    errors.append(error)

        if errors:
            raise MonitorDefinitionsLoadError(errors=[error])

        return monitors_module

    def load_definitions(self) -> List[Monitor]:
        module = self.load_definitions_module()
        monitors: List[Monitor] = module.get_monitors()  # type: ignore
        return monitors

    def get_draft_name(self, monitor: Monitor) -> str:
        return f"[draft] {monitor.name}"

    def insert_libddog_metadata_footer(self, monitor: Monitor) -> None:
        opt_project_phrase = ""
        libddog_link = f"[{self._libddog_proj_name}]({self._libddog_proj_url})"

        output = self.git.get_remotes()
        if output is not None:
            remotes = self.git.parse_remotes(output)
            if remotes:
                name = self.git.get_repo_name(remotes)
                url = self.git.get_repo_http_url(remotes)

                if name and url:
                    opt_project_phrase = (
                        f"is defined in code as part of "
                        f"the [{name}]({url}) project and "
                    )
                elif name:
                    opt_project_phrase = (
                        f"is defined in code as part of the *{name}* project and "
                    )

        content = (
            f"\n\n---\n\n"
            f"This monitor {opt_project_phrase}is maintained automatically "
            f"using the {libddog_link} tool. "
            f"If you make manual changes to it your changes may be lost."
        )

        message = monitor.message or ""
        if content not in message:
            monitor.message = f"{message}{content}"

    def ensure_snapshot_path_exists(self) -> None:
        if not os.path.exists(self.snapshots_path):
            os.makedirs(self.snapshots_path)

    def create_snapshot(self, id: int) -> Path:
        self.ensure_snapshot_path_exists()

        dct = self.client.get_monitor(id=id)

        name = dct.get("name", self._name_sentinel)
        name = sanitize_title_for_filename(name)
        date = format_datetime_for_filename(utcnow())

        block = json.dumps(dct, indent=2, sort_keys=True)
        fn = Path(f"{id}--{name}--{date}.json")
        fp = self.snapshots_path / fn

        with open(fp, "w") as fl:
            fl.write(block)
            fl.write("\n")

        return fp

    # Monitor actions

    def create_monitor(self, monitor: Monitor) -> int:
        self.insert_libddog_metadata_footer(monitor)
        return self.client.create_monitor(monitor=monitor)

    def delete_monitor(self, *, id: int) -> None:
        self.client.delete_monitor(id=id)

    def get_monitor(self, *, id: int) -> JsonDict:
        return self.client.get_monitor(id=id)

    def list_monitors(self) -> List[JsonDict]:
        return self.client.list_monitors()

    def update_monitor(self, monitor: Monitor, id: Optional[int] = None) -> None:
        self.insert_libddog_metadata_footer(monitor)
        self.client.update_monitor(monitor=monitor, id=id)

    def find_first_monitor_with_name(self, name: str) -> Optional[JsonDict]:
        monitor_dicts = self.list_monitors()

        for monitor_dict in monitor_dicts:
            if name == monitor_dict.get("name"):
                return monitor_dict

        return None
