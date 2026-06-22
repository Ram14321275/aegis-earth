from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class OperationalInsight(BaseModel):
    insight_type: str = Field(..., description="e.g., ESCALATION_WARNING, RESOURCE_SATURATION")
    description: str
    action_recommended: str
    urgency_level: str

class TimelineEvent(BaseModel):
    event_id: str
    timestamp: datetime
    hazard_type: str
    severity: str
    location_name: Optional[str] = None
    description: str

class HotspotSummary(BaseModel):
    hotspot_id: str
    region_name: str
    dominant_hazard: str
    threat_score: float
    population_exposed: Optional[int] = None
    infrastructure_risk: str
    escalation_velocity: str = "STABLE" # RAPID, STABLE, DECREASING
    insights: List[OperationalInsight]

class RegionalThreatSummary(BaseModel):
    region_id: str
    region_name: str
    overall_threat_level: str
    active_hotspots: List[HotspotSummary]
    recent_events: List[TimelineEvent]

class GlobalThreatSummary(BaseModel):
    timestamp: datetime
    global_threat_level: str
    critical_regions: List[RegionalThreatSummary]
    global_insights: List[OperationalInsight]

class TimelineSnapshot(BaseModel):
    snapshot_id: str
    parent_snapshot_id: Optional[str] = None
    generated_at: datetime
    revision_number: int
    tenant_id: str
    window_type: str = Field(..., description="1h, 24h, 7d, custom")
    summary: GlobalThreatSummary
