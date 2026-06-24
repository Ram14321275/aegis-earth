# Distributed Edge Topology

Aegis Earth operates as a globally distributed mesh network, eliminating central points of failure.

## Component Overview

### Edge Node Registry
Tracks the health, region, and assignments of all nodes globally.

### Failover Manager
Works directly with `RedisLeaderElection` using `SET NX PX` and `fencing tokens` to ensure only one active primary exists per region, completely mitigating split-brain errors.

### Sovereign Router
Enforces geopolitical routing. Shards traffic explicitly allowing or rejecting packets depending on strict sovereign mapping bounds.

### Degraded Operations
When an edge node drops connection, it immediately transitions to `DEGRADED_MODE`. It starts appending incoming requests to the `OfflineQueue` using local timestamps to later reconcile.
