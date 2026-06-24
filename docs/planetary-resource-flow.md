# Planetary Resource Flow

Aegis Earth unifies:
1. **Forecasting**: Identifying shortfalls 30-90 days out deterministically based on inbound supply vs consumption rates.
2. **Logistics**: The `LogisticsRouter` monitors physical path congestion, triggering re-routes if score thresholds are broken.
3. **Stabilization**: If logistics and supply both fail concurrently, the `EconomicStabilizationEngine` can recommend the release of Strategic Reserves or enact localized Price Controls.
