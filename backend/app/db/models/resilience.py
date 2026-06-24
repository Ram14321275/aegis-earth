from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from app.db.base import TenantAwareModel

class RecoverySession(TenantAwareModel):
    __tablename__ = "recovery_sessions"
    session_id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False)
    target_node = Column(String)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))

class RecoveryCheckpoint(TenantAwareModel):
    __tablename__ = "recovery_checkpoints"
    checkpoint_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("recovery_sessions.session_id"))
    snapshot_hash = Column(String, nullable=False)
    lineage_hash = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class InfrastructureFailure(TenantAwareModel):
    __tablename__ = "infrastructure_failures"
    failure_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class ResilienceEvent(TenantAwareModel):
    __tablename__ = "resilience_events"
    event_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    payload = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SelfHealingAction(TenantAwareModel):
    __tablename__ = "self_healing_actions"
    action_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False) # SAFE_AUTOMATION, APPROVAL_REQUIRED, FORBIDDEN_AUTOMATION
    rollback_strategy = Column(JSON, nullable=False)
    reasoning_hash = Column(String, nullable=False)
    status = Column(String, default="PENDING")
    
class FailoverPromotion(TenantAwareModel):
    __tablename__ = "failover_promotions"
    promotion_id = Column(String, primary_key=True, index=True)
    old_primary = Column(String, nullable=False)
    new_primary = Column(String, nullable=False)
    sovereign_region = Column(String, nullable=False)
    reasoning_hash = Column(String, nullable=False)

class RecoveryVerification(TenantAwareModel):
    __tablename__ = "recovery_verifications"
    verification_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("recovery_sessions.session_id"))
    is_valid = Column(Boolean, nullable=False)
    corruption_detected = Column(Boolean, default=False)

class DegradationState(TenantAwareModel):
    __tablename__ = "degradation_states"
    state_id = Column(String, primary_key=True, index=True)
    mode = Column(String, nullable=False) # READ_ONLY, CACHE_ONLY, etc.
    active = Column(Boolean, default=True)

class MeshNodeHealth(TenantAwareModel):
    __tablename__ = "mesh_node_health"
    node_id = Column(String, primary_key=True, index=True)
    survivability_score = Column(Float, nullable=False)
    status = Column(String, nullable=False)

class RecoveryLineage(TenantAwareModel):
    __tablename__ = "recovery_lineage"
    lineage_id = Column(String, primary_key=True, index=True)
    checkpoint_id = Column(String, ForeignKey("recovery_checkpoints.checkpoint_id"))
    parent_checkpoint_hash = Column(String, nullable=False)
    orchestration_reasoning_hash = Column(String, nullable=False)
    sovereign_region = Column(String, nullable=False)

class SimulationScenario(TenantAwareModel):
    __tablename__ = "simulation_scenarios"
    scenario_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    results = Column(JSON)

class ResilienceViolation(TenantAwareModel):
    __tablename__ = "resilience_violations"
    violation_id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)
    description = Column(String)
