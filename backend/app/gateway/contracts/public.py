from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from app.schemas.intelligence import HazardTypeEnum, SeverityEnum
from app.schemas.geospatial import Coordinates


class ReliabilityMetadata(BaseModel):
    """Metadata detailing the reliability and confidence of the intelligence."""
    overall_confidence: float = Field(..., ge=0.0, le=1.0)
    degraded_providers: List[str] = Field(default_factory=list)
    cache_hit: bool = Field(default=False)
    federation_latency_ms: float
    data_staleness_seconds: int


class HazardCorrelation(BaseModel):
    """Describes causal or statistical relationships between hazards."""
    primary_hazard: HazardTypeEnum
    secondary_hazard: HazardTypeEnum
    correlation_score: float = Field(..., ge=0.0, le=1.0)
    description: str


class ActiveHazard(BaseModel):
    """Represents a localized active hazard."""
    hazard_id: str
    hazard_type: HazardTypeEnum
    severity: SeverityEnum
    confidence: float
    affected_area_km2: float
    bounding_box: List[float] = Field(..., description="[min_lon, min_lat, max_lon, max_lat]", min_length=4, max_length=4)
    last_updated: datetime


class RegionalSummary(BaseModel):
    """Summary of intelligence for a broader geographic region."""
    region_name: str
    overall_risk_score: float = Field(..., ge=0.0, le=100.0)
    active_hazards: List[ActiveHazard]
    correlations: List[HazardCorrelation]


class ThreatTimelineEvent(BaseModel):
    """A point-in-time snapshot of a hazard's evolution."""
    timestamp: datetime
    severity: SeverityEnum
    area_km2: float


class ThreatTimeline(BaseModel):
    """Historical timeline of a specific hazard."""
    hazard_id: str
    events: List[ThreatTimelineEvent]


class GlobalThreatMap(BaseModel):
    """High-level map data for global visualization."""
    heatmap_url: str
    critical_zones: List[Coordinates]


class IntelligenceSnapshot(BaseModel):
    """Unified single-response payload for an intelligence query."""
    snapshot_id: str
    generated_at: datetime
    coordinates: Optional[Coordinates] = None
    regional_summary: Optional[RegionalSummary] = None
    global_map: Optional[GlobalThreatMap] = None
    reliability: ReliabilityMetadata


class StreamingSnapshot(IntelligenceSnapshot):
    """Snapshot designed specifically for websocket real-time feeds."""
    stream_id: str
    is_partial: bool = False


class LiveEventFeed(BaseModel):
    """A single discrete event broadcasted over websockets."""
    event_id: str
    event_type: str
    timestamp: datetime
    payload: Dict[str, Any]


class OperationalHealthSummary(BaseModel):
    """Publicly exposed health metadata."""
    status: str
    gateway_latency_ms: float
    active_connections: int
