import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    INVESTIGATING = "INVESTIGATING"
    ESCALATED = "ESCALATED"
    RESOLVED = "RESOLVED"
    ARCHIVED = "ARCHIVED"


class EscalationStatus(str, Enum):
    PENDING = "PENDING"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    SUPPRESSED = "SUPPRESSED"
    EXPIRED = "EXPIRED"


class TimelineEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    incident_id: str
    actor_id: str
    event_type: str
    details: Dict[str, Any]
    timestamp: datetime = Field(default_factory=utc_now)


class AnalystNote(BaseModel):
    note_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    investigation_id: str
    actor_id: str
    content: str
    evidence_links: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    revision_number: int = 1
    parent_note_id: Optional[str] = None  # For immutable lineage


class EscalationEvent(BaseModel):
    escalation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    incident_id: str
    source_system: str
    severity: str
    status: EscalationStatus = EscalationStatus.PENDING
    cooldown_expires_at: datetime
    correlation_id: str
    reasoning: str
    created_at: datetime = Field(default_factory=utc_now)
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


class WorkflowTask(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    mission_id: str
    assignee_id: Optional[str] = None
    status: str = "PENDING"
    task_type: str
    description: str
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Investigation(BaseModel):
    investigation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    incident_id: str
    lead_analyst_id: Optional[str] = None
    status: str = "ACTIVE"
    summary: str = ""
    revision_number: int = 1
    parent_revision_id: Optional[str] = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    annotations: List[Dict[str, Any]] = Field(default_factory=list)


class Incident(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    status: IncidentStatus = IncidentStatus.OPEN
    severity: str
    confidence: float
    title: str
    description: str
    assigned_analysts: List[str] = Field(default_factory=list)
    linked_hazards: List[str] = Field(default_factory=list)
    linked_snapshots: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    revision_number: int = 1
    parent_revision_id: Optional[str] = None


class CollaborationSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    room_id: str
    active_operators: List[str] = Field(default_factory=list)
    last_sync_at: datetime = Field(default_factory=utc_now)
