# Sovereign Trade Model

All supply chain flows within Aegis Earth pass through the `SovereignTradeEngine`.
- Geopolitical boundaries are modeled as deterministic logic constraints.
- If an allocation engine requests a transfer of fuel from `Region A` to `Region B`, the route is intercepted.
- If `Region A` has an active export restriction against `Region B` for fuel, the transaction is immediately rejected and the violation is recorded.
