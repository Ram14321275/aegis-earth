from app.observability.metrics import metrics_store

class IntelligenceMetricsWrapper:
    """
    Provides a domain-specific interface to the global MetricsStore for the AI Orchestration Layer.
    """
    @staticmethod
    def record_aggregation() -> None:
        metrics_store.record_intelligence_aggregation()
        
    @staticmethod
    def record_correlation(count: int = 1) -> None:
        metrics_store.record_correlation_event(count)
        
    @staticmethod
    def record_explainability(duration_ms: float) -> None:
        metrics_store.record_explainability_generation(duration_ms)
        
    @staticmethod
    def record_prioritization(duration_ms: float) -> None:
        metrics_store.record_prioritization_duration(duration_ms)
        
    @staticmethod
    def record_failure() -> None:
        metrics_store.record_intelligence_failure()

intelligence_metrics = IntelligenceMetricsWrapper()
