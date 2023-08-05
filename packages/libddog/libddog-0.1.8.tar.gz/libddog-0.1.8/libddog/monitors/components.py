from typing import List, Optional

from libddog.common.types import JsonDict
from libddog.monitors.enums import RenotifyStatus


class MonitorThresholds:
    def __init__(
        self,
        *,
        critical: Optional[float] = None,
        critical_recovery: Optional[float] = None,
        ok: Optional[float] = None,
        # unknown: Optional[float] = None,
        warning: Optional[float] = None,
        warning_recovery: Optional[float] = None,
    ):
        self.critical = critical
        self.critical_recovery = critical_recovery
        self.ok = ok
        # self.unknown = unknown
        self.warning = warning
        self.warning_recovery = warning_recovery

    def as_dict(self) -> JsonDict:
        attnames = [
            "critical",
            "critical_recovery",
            "ok",
            # "unknown",  # Datadog API rejects this field
            "warning",
            "warning_recovery",
        ]

        dct = {}
        for attname in attnames:
            value = getattr(self, attname)
            if value is not None:
                dct[attname] = value

        return dct


class MonitorThresholdWindows:
    def __init__(
        self,
        *,
        recovery_window: Optional[str] = None,
        trigger_window: Optional[str] = None,
    ):
        self.recovery_window = recovery_window
        self.trigger_window = trigger_window

    def as_dict(self) -> JsonDict:
        attnames = [
            "recovery_window",
            "trigger_window",
        ]

        dct = {}
        for attname in attnames:
            value = getattr(self, attname)
            if value is not None:
                dct[attname] = value

        return dct


class MonitorOptions:
    def __init__(
        self,
        *,
        enable_logs_sample: Optional[bool] = None,
        escalation_message: Optional[str] = None,
        evaluation_delay: Optional[int] = None,
        # group_retention_duration,
        groupby_simple_monitor: Optional[bool] = False,
        include_tags: Optional[bool] = True,
        # min_failure_duration,
        # min_location_failed,
        new_group_delay: Optional[int] = None,
        no_data_timeframe: Optional[int] = None,
        notify_audit: Optional[bool] = False,
        # notify_by: Optional[List[str]] = None,
        notify_no_data: Optional[bool] = False,
        # on_missing_data: Optional[OnMissingData] = None,
        renotify_interval: Optional[int] = None,
        renotify_occurrences: Optional[int] = None,
        renotify_statuses: Optional[List[RenotifyStatus]] = None,
        require_full_window: Optional[bool] = False,
        # scheduling_options,
        threshold_windows: Optional[MonitorThresholdWindows] = None,
        thresholds: Optional[MonitorThresholds] = None,
        timeout_h: Optional[int] = None,
        # variables,
    ) -> None:
        self.enable_logs_sample = enable_logs_sample
        self.escalation_message = escalation_message
        self.evaluation_delay = evaluation_delay
        self.groupby_simple_monitor = groupby_simple_monitor
        self.include_tags = include_tags
        # self.on_missing_data = on_missing_data or OnMissingData.DEFAULT
        self.new_group_delay = new_group_delay
        self.no_data_timeframe = no_data_timeframe
        self.notify_audit = notify_audit
        # self.notify_by = notify_by
        self.notify_no_data = notify_no_data
        self.renotify_interval = renotify_interval
        self.renotify_occurrences = renotify_occurrences
        self.renotify_statuses = renotify_statuses
        self.require_full_window = require_full_window
        self.threshold_windows = threshold_windows or MonitorThresholdWindows()
        self.thresholds = thresholds or MonitorThresholds()
        self.timeout_h = timeout_h

    def as_dict(self) -> JsonDict:
        renotify_statuses = None
        if self.renotify_statuses:
            renotify_statuses = [status.value for status in self.renotify_statuses]

        threshold_windows: Optional[JsonDict] = self.threshold_windows.as_dict()
        threshold_windows = threshold_windows if threshold_windows else None

        thresholds: Optional[JsonDict] = self.thresholds.as_dict()
        thresholds = thresholds if thresholds else None

        return {
            "enable_logs_sample": self.enable_logs_sample,
            "escalation_message": self.escalation_message,
            "evaluation_delay": self.evaluation_delay,
            "groupby_simple_monitor": self.groupby_simple_monitor,
            "include_tags": self.include_tags,
            # "on_missing_data": self.on_missing_data.value,  # Datadog API rejects this field
            "new_group_delay": self.new_group_delay,
            "no_data_timeframe": self.no_data_timeframe,
            "notify_audit": self.notify_audit,
            # "notify_by": self.notify_by,  # Datadog API rejects this field
            "notify_no_data": self.notify_no_data,
            "renotify_interval": self.renotify_interval,
            "renotify_occurrences": self.renotify_occurrences,
            "renotify_statuses": renotify_statuses,
            "require_full_window": self.require_full_window,
            "threshold_windows": threshold_windows,
            "thresholds": thresholds,
            "timeout_h": self.timeout_h,
        }
