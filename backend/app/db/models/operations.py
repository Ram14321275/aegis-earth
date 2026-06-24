import uuid
from typing import Any, List
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, JSON, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import TenantAwareModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def generate_uuid() -> str:
    return str(uuid.uuid4())


class IncidentModel(TenantAwareModel):
    __tablename__ = "incidents"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    status: Mapped[str] = mapped_column(String, nullable=False, default="OPEN")
    severity: Mapped[str] = mapped_column(String, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    
    assigned_analysts: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    linked_hazards: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    linked_snapshots: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    revision_number: Mapped[int] = mapped_column(Integer, default=1)
    parent_revision_id: Mapped[str | None] = mapped_column(String, nullable=True)


class InvestigationModel(TenantAwareModel):
    __tablename__ = "investigations"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    incident_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    lead_analyst_id: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="ACTIVE")
    summary: Mapped[str] = mapped_column(String, default="")
    
    annotations: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    
    revision_number: Mapped[int] = mapped_column(Integer, default=1)
    parent_revision_id: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)


class AnalystNoteModel(TenantAwareModel):
    __tablename__ = "analyst_notes"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    investigation_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    actor_id: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    evidence_links: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    
    revision_number: Mapped[int] = mapped_column(Integer, default=1)
    parent_note_id: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)


class EscalationEventModel(TenantAwareModel):
    __tablename__ = "escalation_events"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    incident_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    source_system: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="PENDING")
    
    cooldown_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    reasoning: Mapped[str] = mapped_column(String, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    acknowledged_by: Mapped[str | None] = mapped_column(String, nullable=True)
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class MissionWorkflowModel(TenantAwareModel):
    __tablename__ = "mission_workflows"
    
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    mission_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    assignee_id: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="PENDING")
    task_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
