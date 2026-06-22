from app.observability.metrics import metrics_store

class WildfireMetricsWrapper:
    @staticmethod
    def record_analysis_started():
        metrics_store.record_wildfire_analysis_started()

    @staticmethod
    def record_analysis_completed(duration_ms: float):
        metrics_store.record_wildfire_analysis_completed(duration_ms)

    @staticmethod
    def record_alert_generated():
        metrics_store.record_wildfire_alert_generated()

    @staticmethod
    def record_failure():
        metrics_store.record_wildfire_failure()

    @staticmethod
    def record_baseline_cache_hit():
        # Using the existing baseline cache hit metric
        metrics_store.record_baseline_cache_hit()

wildfire_metrics = WildfireMetricsWrapper()
