from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class AlertLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AlertTrigger(BaseModel):
    hazard_type: str
    risk_level: str
    risk_score: float


class AlertMetadata(BaseModel):
    location: str
    confidence: float
    generated_at: str


class Alert(BaseModel):
    severity: AlertLevel
    title: str
    message: str
    confidence: float
    reason: str
    generated_at: datetime
    metadata: AlertMetadata


class AlertSummary(BaseModel):
    alerts: List[Alert]
    highest_severity: AlertLevel
