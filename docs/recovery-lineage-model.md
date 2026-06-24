# Recovery Lineage Model

To maintain replayability through disaster zones:
* A `RecoveryCheckpoint` hashes the current snapshot with the orchestration hash and tenant_id.
* The subsequent checkpoint stores this as `parent_checkpoint_hash`.
* If a snapshot is tampered with on disk, the lineage string breaks.
* The `RecoveryVerificationEngine` will abort any node restore missing a valid cryptographic parent link.
