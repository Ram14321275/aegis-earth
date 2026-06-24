# Supply Chain Lineage

Economic ledgers must be tamper-proof and fully replayable.
- The `ResourceLineageTracker` issues a cryptographic SHA-256 hash for every economic event (Allocation, Transfer, Disruption).
- The hash encodes the event type, resource, amount, and the **parent event hash**.
- This enforces an immutable blockchain-style ledger. If a historical ledger item is tampered with on-disk, the entire chain's recalculation fails.
