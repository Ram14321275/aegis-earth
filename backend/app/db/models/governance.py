from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Boolean
from sqlalchemy.sql import func
from app.db.base import TenantAwareModel

class AuditEvent(TenantAwareModel):
    __tablename__ = "audit_events"
    event_id = Column(String, primary_key=True, index=True)
    actor_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    request_hash = Column(String)
    payload_hash = Column(String, nullable=False)
    reasoning_hash = Column(String)
    parent_event_id = Column(String)
    correlation_id = Column(String)
    lineage_path = Column(String, nullable=False)
    signature = Column(String, nullable=False)
    immutable_sequence_number = Column(Integer, nullable=False)
    signature_algorithm = Column(String, nullable=False)
    signature_version = Column(String, nullable=False)
    key_version = Column(String, nullable=False)

class ApprovalRequest(TenantAwareModel):
    __tablename__ = "approval_requests"
    request_id = Column(String, primary_key=True, index=True)
    requester_id = Column(String, nullable=False)
    action_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, default="PENDING")

class ApprovalDecision(TenantAwareModel):
    __tablename__ = "approval_decisions"
    decision_id = Column(String, primary_key=True, index=True)
    request_id = Column(String, ForeignKey("approval_requests.request_id"))
    approver_id = Column(String, nullable=False)
    decision = Column(String, nullable=False) # APPROVED, REJECTED
    reasoning = Column(String, nullable=False)

class ComplianceExport(TenantAwareModel):
    __tablename__ = "compliance_exports"
    export_id = Column(String, primary_key=True, index=True)
    requester_id = Column(String, nullable=False)
    format = Column(String, nullable=False)
    record_count = Column(Integer, nullable=False)
    status = Column(String, default="COMPLETED")

class RetentionPolicy(TenantAwareModel):
    __tablename__ = "retention_policies"
    policy_id = Column(String, primary_key=True, index=True)
    duration_days = Column(Integer, nullable=False)

class LegalHold(TenantAwareModel):
    __tablename__ = "legal_holds"
    hold_id = Column(String, primary_key=True, index=True)
    reason = Column(String, nullable=False)
    active = Column(Boolean, default=True)

class ReplaySession(TenantAwareModel):
    __tablename__ = "replay_sessions"
    session_id = Column(String, primary_key=True, index=True)
    target_timestamp = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, default="COMPLETED")

class SovereigntyPolicy(TenantAwareModel):
    __tablename__ = "sovereignty_policies"
    policy_id = Column(String, primary_key=True, index=True)
    allowed_regions = Column(JSON, nullable=False)

class GovernanceViolation(TenantAwareModel):
    __tablename__ = "governance_violations"
    violation_id = Column(String, primary_key=True, index=True)
    policy_name = Column(String, nullable=False)
    actor_id = Column(String, nullable=False)
    context_payload = Column(JSON, nullable=False)
