from enum import Enum

from pydantic import BaseModel


class AlertLevel(str, Enum):
    INFO = "info"
    WATCH = "watch"
    WARNING = "warning"
    CRITICAL = "critical"


class Alert(BaseModel):
    title: str
    description: str
    recommendation: str
    level: AlertLevel
