# Resilience Topology

Aegis Earth employs a global mesh designed for active survivability.

1. **Healing Engines**: Monitor node state. Categorize required actions exactly into SAFE, APPROVAL_REQUIRED, and FORBIDDEN.
2. **Sovereign Mesh**: Keeps nodes aware of their geopolitical bounds. Cross-boundary failover is strictly blocked unless an explicit override exists.
3. **Lineage Verifiers**: Ensure that a node rejoining the network hasn't had its checkpoint data corrupted. If hash mismatch occurs, node stays down.
