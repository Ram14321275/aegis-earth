import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any, Literal

from pydantic import BaseModel, Field

from app.schemas.intelligence import SeverityEnum
from app.domain.models.hazard import HazardType


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

class StreamEventType(str, Enum):
    FLOOD = "flood"
    WILDFIRE = "wildfire"
    ENVIRONMENTAL_CHANGE = "environmental_change"
    INTELLIGENCE = "intelligence"
    ALERT = "alert"
    PROVIDERS = "providers"
    INTEGRATIONS = "integrations"
    HUMANITARIAN = "humanitarian"
    DISTRIBUTION = "distribution"
    GOVERNANCE = "governance"
    AUDIT = "audit"
    COMPLIANCE = "compliance"
    APPROVALS = "approvals"
    REPLAY = "replay"
    EDGE_FAILOVER = "edge_failover"
    EDGE_RECOVERY = "edge_recovery"
    RECONCILIATION_EVENT = "reconciliation_event"
    SYNC_CHECKPOINT = "sync_checkpoint"
    CONSISTENCY_VIOLATION = "consistency_violation"
    DEGRADED_MODE = "degraded_mode"
    OFFLINE_RECOVERY = "offline_recovery"
    CYBER_INCIDENT = "cyber_incident"
    THREAT_DETECTED = "threat_detected"
    CONTAINMENT_TRIGGERED = "containment_triggered"
    QUARANTINE_STARTED = "quarantine_started"
    ZERO_TRUST_FAILURE = "zero_trust_failure"
    ATTESTATION_FAILURE = "attestation_failure"
    REPLAY_ATTACK = "replay_attack"
    PROVIDER_COMPROMISE = "provider_compromise"
    THREAT_FEED_UPDATE = "threat_feed_update"
    FORENSIC_REPLAY = "forensic_replay"
    CYBER_SIMULATION = "cyber_simulation"
    RECOVERY_STARTED = "recovery_started"
    RECOVERY_COMPLETED = "recovery_completed"
    FAILOVER_PROMOTED = "failover_promoted"
    SELF_HEALING_TRIGGERED = "self_healing_triggered"
    INFRASTRUCTURE_COLLAPSE = "infrastructure_collapse"
    DEGRADATION_MODE = "degradation_mode"
    RECOVERY_VERIFIED = "recovery_verified"
    MESH_PARTITION = "mesh_partition"
    SIMULATION_COMPLETED = "simulation_completed"
    RECOVERY_ABORTED = "recovery_aborted"

class BaseStreamEvent(BaseModel):
    """
    Mandatory contract for all real-time events published through the Redis broker.
    Provides strict fields for future event replay and distributed tracing.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    generated_at: datetime = Field(default_factory=get_utc_now)
    source: str = Field(..., description="The internal service/worker that produced the event.")
    correlation_id: Optional[str] = Field(default=None, description="ID connecting cascading events.")
    event_version: str = Field(default="1.0")
    
    event_type: StreamEventType
    hazard_type: Optional[HazardType] = None
    severity: Optional[SeverityEnum] = None
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    
    # Optional region bounding / location identifier
    location_id: Optional[str] = None
    region_metadata: Dict[str, Any] = Field(default_factory=dict)


class FloodEvent(BaseStreamEvent):
    event_type: Literal[StreamEventType.FLOOD] = StreamEventType.FLOOD
    hazard_type: Literal[HazardType.FLOOD] = HazardType.FLOOD
    water_level_m: Optional[float] = None
    affected_area_km2: float


class WildfireEvent(BaseStreamEvent):
    event_type: Literal[StreamEventType.WILDFIRE] = StreamEventType.WILDFIRE
    hazard_type: Literal[HazardType.WILDFIRE] = HazardType.WILDFIRE
    burn_index: Optional[float] = None
    active_fire_pixels: int


class EnvironmentalChangeEvent(BaseStreamEvent):
    event_type: Literal[StreamEventType.ENVIRONMENTAL_CHANGE] = StreamEventType.ENVIRONMENTAL_CHANGE
    hazard_type: Literal[HazardType.ENVIRONMENTAL_CHANGE] = HazardType.ENVIRONMENTAL_CHANGE
    change_type: str  # e.g., "vegetation_loss", "urban_expansion"
    temporal_window: str


class IntelligenceEvent(BaseStreamEvent):
    """
    Streaming envelope for Cross-Hazard correlations and AI Explainability updates.
    """
    event_type: Literal[StreamEventType.INTELLIGENCE] = StreamEventType.INTELLIGENCE
    contributing_indicators: List[str] = Field(default_factory=list)
    reasoning_summary: str
    

class AlertEvent(BaseStreamEvent):
    """
    Streaming envelope for escalated tactical alerts.
    """
    event_type: Literal[StreamEventType.ALERT] = StreamEventType.ALERT
    alert_id: str
    message: str
    recommended_action: Optional[str] = None


class ClientSubscription(BaseModel):
    """
    Defines the filter rules for a specific WebSocket connection.
    Client can dynamically update this payload over the WebSocket.
    """
    regions: List[str] = Field(default_factory=list, description="List of location_ids.")
    hazard_types: List[HazardType] = Field(default_factory=list)
    min_severity: Optional[SeverityEnum] = None
    intelligence_categories: List[StreamEventType] = Field(default_factory=list)
