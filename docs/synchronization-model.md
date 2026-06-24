# Synchronization & Reconciliation Model

Aegis Earth prioritizes determinism over blind consensus.

## Deterministic Replication

* Edge Checkpoints track the exact event ID last processed.
* Replayability rules demand no gaps in lineage. If an event is received that does not match the parent ID, it triggers a `ConsistencyViolation`.

## Conflict Resolution

We use explicit conflict arbitration without arbitrary Last-Write-Wins (LWW) overrides unless mathematically determined.

* **Timestamp Arbitration**: Oldest timestamp wins.
* **Hash Break**: If timestamps match, the lowest payload hash lexicographically wins.
* All resolutions yield a `ReconciliationEvent` pointing to both divergent branch hashes.
