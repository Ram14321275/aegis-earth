from typing import Dict, Any
from app.observability.metrics import metrics_store

class ResilienceTelemetry:
    """Tracks infrastructure recovery and mesh health."""
    
    @staticmethod
    def update_mesh_score(score: float):
        # We can hijack a resilience metric to store the current score
        # For a counter-based system, we'll assume the metric gets overridden or logged.
        metrics_store.record_resilience_action("mesh_survivability_score", score - metrics_store.resilience_metrics.get("mesh_survivability_score", 100))

    @staticmethod
    def record_abort():
        metrics_store.record_resilience_action("restoration_aborts_total")

resilience_telemetry = ResilienceTelemetry()
