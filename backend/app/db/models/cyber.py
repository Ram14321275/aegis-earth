from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from app.db.base import TenantAwareModel

class CyberIncident(TenantAwareModel):
    __tablename__ = "cyber_incidents"
    incident_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    lineage_hash = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ThreatIndicator(TenantAwareModel):
    __tablename__ = "threat_indicators"
    indicator_id = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)
    type = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    confidence_degradation_reason = Column(String)

class ThreatSignal(TenantAwareModel):
    __tablename__ = "threat_signals"
    signal_id = Column(String, primary_key=True, index=True)
    source = Column(String, nullable=False)
    deterministic_reason_codes = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ThreatDetection(TenantAwareModel):
    __tablename__ = "threat_detections"
    detection_id = Column(String, primary_key=True, index=True)
    signal_id = Column(String, ForeignKey("threat_signals.signal_id"))
    reasoning_hash = Column(String, nullable=False)

class ContainmentAction(TenantAwareModel):
    __tablename__ = "containment_actions"
    action_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    rollback_strategy = Column(JSON, nullable=False)
    approval_required = Column(Boolean, default=False)
    reversible_until = Column(DateTime(timezone=True))
    lineage_hash = Column(String, nullable=False)
    status = Column(String, default="PENDING")

class QuarantineSession(TenantAwareModel):
    __tablename__ = "quarantine_sessions"
    session_id = Column(String, primary_key=True, index=True)
    target_id = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), server_default=func.now())

class ServiceIdentity(TenantAwareModel):
    __tablename__ = "service_identities"
    identity_id = Column(String, primary_key=True, index=True)
    service_name = Column(String, nullable=False)
    sovereign_region = Column(String, nullable=False)
    public_key = Column(String, nullable=False)

class EdgeAttestation(TenantAwareModel):
    __tablename__ = "edge_attestations"
    attestation_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, nullable=False)
    nonce = Column(String, nullable=False)
    signature = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ThreatFeed(TenantAwareModel):
    __tablename__ = "threat_feeds"
    feed_id = Column(String, primary_key=True, index=True)
    source = Column(String, nullable=False)
    indicators = Column(JSON, nullable=False)

class ThreatReplay(TenantAwareModel):
    __tablename__ = "threat_replays"
    replay_id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("cyber_incidents.incident_id"))
    replay_reference = Column(String, nullable=False)

class CyberSimulation(TenantAwareModel):
    __tablename__ = "cyber_simulations"
    simulation_id = Column(String, primary_key=True, index=True)
    scenario_type = Column(String, nullable=False)
    results = Column(JSON)

class ThreatCampaign(TenantAwareModel):
    __tablename__ = "threat_campaigns"
    campaign_id = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=False)
    related_incidents = Column(JSON)

class ThreatEvidence(TenantAwareModel):
    __tablename__ = "threat_evidence"
    evidence_id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("cyber_incidents.incident_id"))
    payload = Column(JSON, nullable=False)
    hash = Column(String, nullable=False)
