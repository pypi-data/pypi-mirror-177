import enum


class RenotifyStatus(enum.Enum):
    ALERT = "alert"
    WARN = "warn"
    NO_DATA = "no data"


class OnMissingData(enum.Enum):
    DEFAULT = "default"
    SHOW_NO_DATA = "show_no_data"
    SHOW_AND_NOTIFY_NO_DATA = "show_and_notify_no_data"
    RESOLVE = "resolve"
