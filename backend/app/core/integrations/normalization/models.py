from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class NormalizedSeverity(BaseModel):
    level: str = Field(description="Canonical severity: INFO, WARNING, HIGH, CRITICAL")
    score: float = Field(ge=0.0, le=1.0)

class CanonicalHazardEvent(BaseModel):
    event_type: str = Field(description="E.g., WILDFIRE, FLOOD, EARTHQUAKE")
    timestamp: datetime
    latitude: float
    longitude: float
    severity: NormalizedSeverity
    confidence: float = Field(ge=0.0, le=1.0)
    provider_source: str
    original_event_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
