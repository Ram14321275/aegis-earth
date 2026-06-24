# Incident Response Flow

1. **Signal Generation**: Sensors (`ws/router`, `api_keys`) drop signals into the `CyberDetectionEngine`.
2. **Deterministic Evaluation**: Weights are applied. ML engines are completely bypassed. Reason codes are bundled.
3. **Triggered Containment**: The `ContainmentEngine` spins up an Action.
   - If enterprise tenant = `True`, action is queued for human approval.
   - Otherwise, `status` becomes `EXECUTED`.
4. **Reversible Path**: Actions hold a `rollback_strategy`. Operators can revert the posture back instantly through the dashboard.
5. **Replay Forensics**: `ForensicEngine` takes the lineage sequence and allows exact step-by-step playback of the breach.
