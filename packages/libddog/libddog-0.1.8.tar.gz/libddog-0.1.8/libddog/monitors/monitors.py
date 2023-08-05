from typing import List, Optional

from libddog.common.types import JsonDict
from libddog.monitors.bases import AlertQuery
from libddog.monitors.components import MonitorOptions
from libddog.monitors.event_v2_alert_query import EventV2AlertQueryMonad
from libddog.monitors.metric_alert_query import MetricAlertQueryMonad


class Monitor:
    def __init__(
        self,
        *,
        id: Optional[int] = None,
        name: str,
        message: str,
        query: AlertQuery,
        options: Optional[MonitorOptions] = None,
        priority: Optional[int] = None,
        restricted_roles: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.message = message
        self.query = query
        self.options = options or MonitorOptions()
        self.priority = priority
        self.restricted_roles = restricted_roles
        self.tags = tags or []

        self.type_name = "unsupported"
        self.type_desc = "Unsupported"

        if isinstance(self.query, MetricAlertQueryMonad):
            self.type_name = "query alert"
            self.type_desc = "Metric"
        elif isinstance(self.query, EventV2AlertQueryMonad):
            self.type_name = "event-v2 alert"
            self.type_desc = "Event"

    def as_dict(self) -> JsonDict:
        return {
            "id": self.id,
            "name": self.name,
            "message": self.message,
            "query": self.query.codegen(),
            "options": self.options.as_dict(),
            "priority": self.priority,
            "restricted_roles": self.restricted_roles,
            "tags": self.tags,
            "type": self.type_name,
        }
