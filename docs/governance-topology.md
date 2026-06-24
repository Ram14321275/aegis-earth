# Sovereign Intelligence Governance Topology

The Sovereign Governance Layer in Aegis Earth ensures that every action is cryptographically auditable, compliant with geographic sovereignty laws, and deterministically reconstructable without relying on opaque ML systems.

## Component Overview

1. **Immutable Audit Engine (`backend/app/core/governance/audit/`)**
   - Cryptographically hashes and signs every action using HMAC SHA-256.
   - Preserves lineage using chained hashes.

2. **Governance Policy Engine (`backend/app/core/governance/policies/`)**
   - Deterministically evaluates geographical rules, sharing boundaries, and operator privileges.

3. **Approval Workflow System (`backend/app/core/governance/approvals/`)**
   - Gates destructive and critical actions behind multi-party authorization chains.

4. **Sovereignty Boundary Resolver (`backend/app/core/governance/sovereignty/`)**
   - Blocks prohibited cross-border intel exports via explicit tenant isolation models.

5. **Compliance Export Engine (`backend/app/core/governance/compliance/`)**
   - Orchestrates async generation of signed JSON, CSV, and GeoJSON evidence bundles.

6. **Retention & Archival Engine (`backend/app/core/governance/retention/`)**
   - Manages indefinite legal holds and tenant-specific expiration rules without blind deletion.

7. **Forensic Replay Engine (`backend/app/core/governance/replay/`)**
   - Reconstructs operational intelligence deterministically from historical snapshots.

## Data Flow

- **Incoming Action** -> Evaluated by `GovernancePolicyEngine`.
- **If Critical** -> Intercepted by `ApprovalWorkflowEngine`.
- **If Export** -> Validated by `SovereigntyBoundaryResolver`.
- **Upon Execution** -> Signed and chained via `ImmutableAuditEngine`.
- **Over Time** -> Audited via `ComplianceExportEngine` and managed by `RetentionEngine`.
- **During Investigation** -> Inspected via `ForensicReplayEngine`.
