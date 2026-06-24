# Disruption Propagation Model

Instead of utilizing non-deterministic neural networks to guess at cascading outages, Aegis Earth uses the `EconomicDisruptionEngine`.
- Propagation is determined strictly by the initial root severity and the depth of the dependency tree.
- A severity of 0.8 with 5 dependencies yields a deterministic maximum impact score, tracing 5 steps down the lineage graph to alert downstream regions.
