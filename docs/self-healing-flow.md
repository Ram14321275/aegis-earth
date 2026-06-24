# Self-Healing Flow

1. An infrastructure stress event occurs (e.g. queue depth explodes).
2. The `StabilizationEngine` evaluates deterministically.
3. It emits a recommendation array: `[queue_pressure_stabilization]`.
4. The `ResilienceOrchestrator` consumes the recommendation and passes it to the `SelfHealingEngine`.
5. The healing engine categorizes it. If it is `SAFE_AUTOMATION` (e.g. clear cache), it executes immediately and tracks a rollback strategy.
6. If it is a hard restart, it gets placed in `PENDING_APPROVAL` for Governance.
