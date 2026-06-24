from sqlalchemy import String, Integer, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from typing import Any, Dict
from datetime import datetime

from app.db.base import TenantAwareModel, BaseModel

class ExternalProvider(TenantAwareModel):
    __tablename__ = "external_providers"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider_type: Mapped[str] = mapped_column(String(50), nullable=False) # weather, cap, infrastructure, etc.
    base_url: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    auth_config: Mapped[Dict[str, Any] | None] = mapped_column(JSON, nullable=True) # encrypted/hashed tokens
    tier: Mapped[int] = mapped_column(Integer, default=2) # 1=Critical, 2=Enrichment

class ProviderHealth(TenantAwareModel):
    __tablename__ = "provider_health"

    provider_id: Mapped[str] = mapped_column(ForeignKey("external_providers.id"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False) # healthy, degraded, failing
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    last_check_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class ProviderCapability(TenantAwareModel):
    __tablename__ = "provider_capabilities"

    provider_id: Mapped[str] = mapped_column(ForeignKey("external_providers.id"), index=True, nullable=False)
    capability: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)

class ExternalEvent(TenantAwareModel):
    __tablename__ = "external_events"

    provider_id: Mapped[str] = mapped_column(ForeignKey("external_providers.id"), index=True, nullable=False)
    source_event_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    raw_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    ingestion_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String, index=True, nullable=True)

class NormalizedEvent(TenantAwareModel):
    __tablename__ = "normalized_events"

    external_event_id: Mapped[str] = mapped_column(ForeignKey("external_events.id"), unique=True, nullable=False)
    canonical_type: Mapped[str] = mapped_column(String(50), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    reconciled_payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    normalization_version: Mapped[str] = mapped_column(String(50), nullable=False)

class IngestionFailure(TenantAwareModel):
    __tablename__ = "ingestion_failures"

    provider_id: Mapped[str] = mapped_column(ForeignKey("external_providers.id"), nullable=True)
    raw_payload: Mapped[str] = mapped_column(Text, nullable=False)
    error_reason: Mapped[str] = mapped_column(Text, nullable=False)
    quarantine_status: Mapped[str] = mapped_column(String(50), default="quarantined")

class WebhookDelivery(TenantAwareModel):
    __tablename__ = "webhook_deliveries"

    target_url: Mapped[str] = mapped_column(String, nullable=False)
    payload: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False) # pending, delivered, failed
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class HumanitarianRequest(TenantAwareModel):
    __tablename__ = "humanitarian_requests"

    provider_id: Mapped[str] = mapped_column(ForeignKey("external_providers.id"), nullable=False)
    request_type: Mapped[str] = mapped_column(String(100), nullable=False) # resource, shelter, routing
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    details: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="open")

class InteroperabilityExport(TenantAwareModel):
    __tablename__ = "interoperability_exports"

    format: Mapped[str] = mapped_column(String(50), nullable=False) # cap, geojson, stac, etc
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    lineage_refs: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending")

class ReplayRecord(TenantAwareModel):
    __tablename__ = "replay_records"

    target_type: Mapped[str] = mapped_column(String(50), nullable=False) # provider, webhook, etc.
    target_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="queued")
    result: Mapped[Dict[str, Any] | None] = mapped_column(JSON, nullable=True)
