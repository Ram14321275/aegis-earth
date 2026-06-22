from app.observability.metrics import metrics_store

class TemporalMetricsWrapper:
    """
    Provides a domain-specific interface to the global MetricsStore for Temporal Change Detection.
    """
    @staticmethod
    def record_analysis_completed(duration_ms: float) -> None:
        metrics_store.record_temporal_analysis(duration_ms)
        
    @staticmethod
    def record_failure() -> None:
        metrics_store.record_temporal_failure()
        
    @staticmethod
    def record_cache_hit() -> None:
        metrics_store.record_temporal_cache_hit()
        
    @staticmethod
    def update_queue_depth(depth: int) -> None:
        metrics_store.update_temporal_queue_depth(depth)
        
    @staticmethod
    def record_job_duration(duration_ms: float) -> None:
        metrics_store.record_temporal_job_duration(duration_ms)
        
    @staticmethod
    def record_scene_fetch(duration_ms: float) -> None:
        metrics_store.record_temporal_scene_fetch(duration_ms)
        
    @staticmethod
    def record_geojson_size(size_bytes: int) -> None:
        metrics_store.record_temporal_geojson_size(size_bytes)

temporal_metrics = TemporalMetricsWrapper()
