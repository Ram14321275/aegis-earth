from app.observability.metrics import metrics_store

class StreamingMetricsWrapper:
    """
    Domain-specific wrapper for streaming telemetry.
    """
    @staticmethod
    def record_websocket_disconnect(is_backpressure: bool = False):
        metrics_store.record_websocket_disconnect(is_backpressure)
        
    @staticmethod
    def record_pubsub_failure(delivery: bool = False):
        metrics_store.record_pubsub_failure(delivery)

streaming_metrics = StreamingMetricsWrapper()
