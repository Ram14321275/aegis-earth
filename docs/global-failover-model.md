# Global Failover Model

When a region primary dies:
1. `FailoverPromoter` acquires Redis leases.
2. It generates a new monotonic `fencing_token`.
3. It validates the new primary through `SovereignFencing`.
4. The promotion event is broadcasted via websockets (`/ws/failover`) and metrics updated.
5. Split-brain is prevented as the older generation node will have its stale fencing token rejected by the cluster.
