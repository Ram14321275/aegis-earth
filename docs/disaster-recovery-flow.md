# Disaster Recovery & Survivability Flow

## Recovery Scenario: Regional Outage

1. **Failure Detection**: Heartbeat misses trigger the `FailoverManager`.
2. **Leader Election**: Fallback node initiates a Redis lease lock attempt.
3. **Split Brain Prevention**: If fallback cannot acquire lease (network partition, not outage), it enters Degraded Mode.
4. **Offline Queueing**: Degraded node queues operations locally in `OfflineQueue`.
5. **Reconnection**:
    - `RecoveryEngine` validates queued lineage.
    - Queued events are pushed to the `SynchronizationOrchestrator`.
    - Conflicts handled via `ConflictResolutionEngine`.
6. **Restoration**: Node state returns to `ACTIVE`.
