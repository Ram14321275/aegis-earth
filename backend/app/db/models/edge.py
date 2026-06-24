from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, Integer, Boolean
from sqlalchemy.sql import func
from app.db.base import TenantAwareModel

class EdgeNode(TenantAwareModel):
    __tablename__ = "edge_nodes"
    node_id = Column(String, primary_key=True, index=True)
    sovereign_region = Column(String, nullable=False)
    jurisdiction = Column(String, nullable=False)
    health_state = Column(String, nullable=False, default="ACTIVE")
    synchronization_state = Column(String, nullable=False, default="IN_SYNC")
    latency_profile = Column(String)

class EdgeCheckpoint(TenantAwareModel):
    __tablename__ = "edge_checkpoints"
    checkpoint_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("edge_nodes.node_id"), nullable=False)
    last_event_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SynchronizationSession(TenantAwareModel):
    __tablename__ = "synchronization_sessions"
    session_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("edge_nodes.node_id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    events_synced = Column(Integer, default=0)

class ReconciliationEvent(TenantAwareModel):
    __tablename__ = "reconciliation_events"
    event_id = Column(String, primary_key=True, index=True)
    base_hash = Column(String, nullable=False)
    branch_a_hash = Column(String, nullable=False)
    branch_b_hash = Column(String, nullable=False)
    resolved_hash = Column(String, nullable=False)
    policy_used = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SovereignPartition(TenantAwareModel):
    __tablename__ = "sovereign_partitions"
    partition_id = Column(String, primary_key=True, index=True)
    region_name = Column(String, nullable=False)
    allowed_tenants = Column(JSON, nullable=False)

class ReplayCheckpoint(TenantAwareModel):
    __tablename__ = "replay_checkpoints"
    checkpoint_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("edge_nodes.node_id"), nullable=False)
    replay_event_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class FailoverEvent(TenantAwareModel):
    __tablename__ = "failover_events"
    event_id = Column(String, primary_key=True, index=True)
    failed_node_id = Column(String, nullable=False)
    promoted_node_id = Column(String, nullable=False)
    region = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class OfflineQueue(TenantAwareModel):
    __tablename__ = "offline_queues"
    queue_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("edge_nodes.node_id"), nullable=False)
    event_payload = Column(JSON, nullable=False)
    offline_timestamp = Column(DateTime(timezone=True), nullable=False)

class EdgeConsistencyViolation(TenantAwareModel):
    __tablename__ = "edge_consistency_violations"
    violation_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("edge_nodes.node_id"), nullable=False)
    description = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class RecoverySession(TenantAwareModel):
    __tablename__ = "recovery_sessions"
    session_id = Column(String, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("edge_nodes.node_id"), nullable=False)
    status = Column(String, nullable=False) # e.g. COMPLETED, FAILED
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
