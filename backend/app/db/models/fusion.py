from datetime import datetime
from sqlalchemy import String, Float, Integer, Boolean, JSON, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import TenantAwareModel

class FusedRegionalAssessment(TenantAwareModel):
    __tablename__ = "fused_regional_assessments"

    # Lineage tracking
    lineage_id: Mapped[str] = mapped_column(String, index=True)
    correlation_id: Mapped[str] = mapped_column(String, index=True)
    
    # Hierarchical Rollups
    aggregation_level: Mapped[str] = mapped_column(String, index=True) # local, district, state, country, continental, global
    region_id: Mapped[str] = mapped_column(String, index=True)
    parent_region_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    
    # Intelligence Output
    fused_score: Mapped[float] = mapped_column(Float)
    threat_level: Mapped[str] = mapped_column(String)
    
    # Explainability Data
    fusion_explanation: Mapped[dict] = mapped_column(JSON) # Stores FusionExplanation model
    contributing_hazards: Mapped[list] = mapped_column(JSON)
    
    # Event Sourcing
    event_version: Mapped[int] = mapped_column(Integer, default=1)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class CorrelationEvent(TenantAwareModel):
    __tablename__ = "correlation_events"
    
    correlation_event_id: Mapped[str] = mapped_column(String, index=True)
    primary_hazard_id: Mapped[str] = mapped_column(String, index=True)
    secondary_hazard_id: Mapped[str] = mapped_column(String, index=True)
    
    interaction_type: Mapped[str] = mapped_column(String) # e.g. "amplification", "suppression"
    amplification_factor: Mapped[float] = mapped_column(Float)
    
    # Cooldown enforcement
    cooldown_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ReliabilitySnapshot(TenantAwareModel):
    __tablename__ = "reliability_snapshots"
    
    snapshot_id: Mapped[str] = mapped_column(String, index=True)
    source_hazard_id: Mapped[str] = mapped_column(String, index=True)
    
    # Separation of raw vs adjusted
    raw_score: Mapped[float] = mapped_column(Float)
    reliability_adjusted_score: Mapped[float] = mapped_column(Float)
    reliability_score: Mapped[float] = mapped_column(Float)
    
    # Drift Detection
    provider_source: Mapped[str] = mapped_column(String, index=True)
    provider_degraded: Mapped[bool] = mapped_column(Boolean, default=False)
    degradation_reasons: Mapped[list] = mapped_column(JSON)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class EscalationEvent(TenantAwareModel):
    __tablename__ = "escalation_events"
    
    escalation_id: Mapped[str] = mapped_column(String, index=True)
    region_id: Mapped[str] = mapped_column(String, index=True)
    
    escalation_level: Mapped[str] = mapped_column(String) # advisory, elevated, severe, emergency, catastrophic
    trigger_reason: Mapped[str] = mapped_column(String)
    
    # Link to the fused assessment that triggered this
    fused_assessment_id: Mapped[str] = mapped_column(String, ForeignKey("fused_regional_assessments.id"))
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AnomalyRecord(TenantAwareModel):
    __tablename__ = "anomaly_records"
    
    anomaly_id: Mapped[str] = mapped_column(String, index=True)
    source_hazard_id: Mapped[str] = mapped_column(String, index=True)
    
    anomaly_type: Mapped[str] = mapped_column(String) # "impossible_jump", "corrupted_output", "sudden_collapse"
    details: Mapped[dict] = mapped_column(JSON)
    suppressed: Mapped[bool] = mapped_column(Boolean, default=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
