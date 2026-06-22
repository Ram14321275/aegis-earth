from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AggregationHierarchy(BaseModel):
    level: str = Field(..., description="local, district, state, country, continental, global")
    region_id: str
    parent_region_id: Optional[str] = None

class FusionExplanation(BaseModel):
    reasoning_summary: str
    contributing_hazards: List[str]
    weights: Dict[str, float]
    suppression_reasons: List[str] = Field(default_factory=list)
    temporal_stabilization_effects: List[str] = Field(default_factory=list)

class RegionalThreatAssessment(BaseModel):
    lineage_id: str
    correlation_id: str
    aggregation_hierarchy: AggregationHierarchy
    fused_score: float = Field(..., ge=0.0, le=100.0)
    threat_level: str
    explanation: FusionExplanation
    event_version: int = 1
    timestamp: datetime

class CascadingRisk(BaseModel):
    correlation_event_id: str
    primary_hazard_id: str
    secondary_hazard_id: str
    interaction_type: str
    amplification_factor: float
    cooldown_expires_at: Optional[datetime]
    timestamp: datetime

class ReliabilityAssessment(BaseModel):
    snapshot_id: str
    source_hazard_id: str
    raw_score: float = Field(..., ge=0.0, le=100.0)
    reliability_adjusted_score: float = Field(..., ge=0.0, le=100.0)
    reliability_score: float = Field(..., ge=0.0, le=100.0)
    provider_source: str
    provider_degraded: bool = False
    degradation_reasons: List[str] = Field(default_factory=list)
    timestamp: datetime

class EscalationEvent(BaseModel):
    escalation_id: str
    region_id: str
    escalation_level: str = Field(..., description="advisory, elevated, severe, emergency, catastrophic")
    trigger_reason: str
    fused_assessment_id: str
    timestamp: datetime

class GlobalRiskSummary(BaseModel):
    lineage_id: str
    global_priority_score: float = Field(..., ge=0.0, le=100.0)
    active_escalations: int
    critical_regions: List[str]
    timestamp: datetime

class IntelligenceAnomaly(BaseModel):
    anomaly_id: str
    source_hazard_id: str
    anomaly_type: str = Field(..., description="impossible_jump, corrupted_output, sudden_collapse")
    details: Dict[str, Any]
    suppressed: bool = True
    timestamp: datetime
