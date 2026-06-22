import threading
from typing import Dict

from app.schemas.observability import (
    AlertMetrics,
    AnalysisMetrics,
    APIMetrics,
    CacheMetrics,
    DatabaseMetrics,
    SpatialMetrics,
    SatelliteMetrics,
    GEEMetrics,
    ProcessingMetrics,
    SystemMetricsResponse,
    VisualizationMetrics,
    JobMetrics,
    WorkerMetrics,
    FloodMetrics,
    WildfireMetrics,
    TemporalMetrics,
    IntelligenceMetrics,
    StreamingMetrics,
    FusionMetrics,
    GatewayMetrics,
    TileMetrics,
    CommandCenterMetrics,
    PredictiveMetrics,
    InfrastructurePredictionMetrics,
    AutonomousRemediationMetrics,
)


class MetricsStore:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MetricsStore, cls).__new__(cls)
                cls._instance._init_metrics()
        return cls._instance

    def _init_metrics(self):
        # API
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.total_latency_ms = 0.0

        # Cache & Redis
        self.cache_hits_total = 0
        self.cache_misses_total = 0
        self.redis_lock_acquired_total = 0
        self.redis_lock_wait_total_ms = 0.0
        self.redis_errors_total = 0

        # Analysis
        self.total_analyses = 0
        self.hazard_breakdown: Dict[str, int] = {}
        self.total_risk_score = 0.0

        # Alerts
        self.alerts_generated_total = 0
        self.alerts_high_total = 0
        self.alerts_critical_total = 0
        self.alerts_generation_ms = 0.0

        # Visualizations
        self.visualization_requests_total = 0
        self.visualization_generation_ms = 0.0

        # Database
        self.db_queries_total = 0
        self.db_query_duration_ms = 0.0
        self.db_failures_total = 0

        # Spatial
        self.spatial_queries_total = 0
        self.spatial_query_duration_ms = 0.0
        self.spatial_query_failures_total = 0
        
        # Satellite
        self.satellite_requests_total = 0
        self.satellite_cache_hits_total = 0
        self.satellite_provider_failures_total = 0
        self.satellite_fetch_duration_ms = 0.0

        # GEE
        self.gee_requests_total = 0
        self.gee_cache_hits_total = 0
        self.gee_failures_total = 0
        self.gee_retry_total = 0
        self.gee_request_duration_ms = 0.0

        # Jobs & Workers
        self.jobs_created_total = 0
        self.jobs_completed_total = 0
        self.jobs_failed_total = 0
        self.jobs_retried_total = 0
        self.jobs_cancelled_total = 0
        self.queue_depth = 0
        self.job_queue_depth = 0
        self.deduplication_saves_total = 0
        self.recovered_jobs_total = 0
        self.stale_job_requeues_total = 0
        self.idempotency_reuse_total = 0
        self.queue_wait_duration_ms = 0.0
        self.workers_active_total = 0
        self.worker_failures_total = 0
        self.worker_execution_time_ms = 0.0
        self.worker_execution_duration_ms = 0.0
        self.worker_utilization_ratio = 0.0

        # Processing
        self.processing_jobs_total = 0
        self.processing_failures_total = 0
        self.processing_duration_ms = 0.0
        self.sentinel1_processed_total = 0
        self.sentinel2_processed_total = 0
        self.indices_generated_total = 0

        # Flood
        self.flood_analyses_total = 0
        self.flood_detections_total = 0
        self.flood_detection_duration_ms = 0.0
        self.flood_high_risk_total = 0
        self.flood_critical_total = 0
        self.baseline_cache_hits_total = 0

        # Wildfire
        self.wildfire_analyses_total = 0
        self.wildfire_processing_time_ms = 0.0
        self.wildfire_alerts_generated = 0
        self.wildfire_failures = 0
        # Temporal
        self.temporal_analyses_total = 0
        self.temporal_processing_duration_ms = 0.0
        self.change_detection_failures = 0
        self.temporal_cache_hits = 0
        self.temporal_queue_depth = 0
        self.temporal_job_duration_ms = 0.0
        self.temporal_scene_fetch_duration_ms = 0.0
        self.temporal_geojson_size_bytes = 0

        # Intelligence
        self.intelligence_aggregations_total = 0
        self.correlation_events_total = 0
        self.explainability_generation_ms = 0.0
        self.prioritization_duration_ms = 0.0
        self.intelligence_failures = 0

        # Streaming
        self.active_websocket_connections = 0
        self.websocket_messages_total = 0
        self.websocket_disconnects_total = 0
        self.websocket_queue_overflows_total = 0
        self.websocket_backpressure_disconnects_total = 0
        self.pubsub_failures_total = 0
        self.pubsub_delivery_failures_total = 0
        self.streaming_latency_ms = 0.0
        self.streaming_events_total = 0
        self.streaming_total_size_bytes = 0

        # Fusion
        self.fusion_operations_total = 0
        self.escalation_events_total = 0
        self.anomaly_flags_total = 0
        self.reliability_degradations_total = 0
        self.cascading_events_detected = 0
        self.regional_aggregation_duration_ms = 0.0
        self.fusion_processing_duration_ms = 0.0

        # Gateway
        self.federated_requests_total = 0
        self.coalesced_requests_total = 0
        self.provider_timeout_total = 0
        self.degraded_responses_total = 0
        self.websocket_broadcast_latency_ms = 0.0

        # Tiles
        self.tile_generation_duration_ms = 0.0
        self.vector_tiles_total = 0
        self.raster_tiles_total = 0
        self.vector_tile_size_bytes = 0
        self.raster_tile_size_bytes = 0
        self.tile_cache_hits_total = 0
        self.geometry_simplification_savings_bytes = 0
        self.websocket_tile_broadcasts_total = 0

        # Command Center
        self.command_center_metrics = {
            "timeline_generation_duration_ms": 0.0,
            "timeline_queries_total": 0,
            "timeline_cache_hits_total": 0,
            "hotspot_refresh_total": 0,
            "snapshot_generation_duration_ms": 0.0,
            "snapshot_persistence_duration_ms": 0.0,
            "export_jobs_total": 0,
            "export_failures_total": 0,
            "replay_sessions_total": 0,
            "websocket_timeline_connections": 0,
            "command_center_active_streams": 0
        }

        # Predictive Intelligence
        self.predictive_metrics = {
            "forecast_generation_total": 0,
            "forecast_failures_total": 0,
            "anomaly_detection_total": 0,
            "simulation_duration_ms": 0.0,
            "predictive_cache_hits": 0,
            "predictive_queue_depth": 0,
            "infrastructure_forecast_duration_ms": 0.0,
            "autonomous_remediations_total": 0,
            "remediation_failures_total": 0
        }

        self._metrics_lock = threading.Lock()

    def record_api_request(self, success: bool, latency_ms: float):
        with self._metrics_lock:
            self.total_requests += 1
            if success:
                self.successful_requests += 1
            else:
                self.failed_requests += 1
            self.total_latency_ms += latency_ms

    def record_cache_access(self, hit: bool):
        with self._metrics_lock:
            if hit:
                self.cache_hits_total += 1
            else:
                self.cache_misses_total += 1

    def record_redis_lock(self, acquired: bool, wait_ms: float = 0.0):
        with self._metrics_lock:
            if acquired:
                self.redis_lock_acquired_total += 1
            self.redis_lock_wait_total_ms += wait_ms

    def record_redis_error(self):
        with self._metrics_lock:
            self.redis_errors_total += 1

    def record_analysis(self, hazard_type: str, risk_score: float):
        with self._metrics_lock:
            self.total_analyses += 1
            self.total_risk_score += risk_score
            self.hazard_breakdown[hazard_type] = (
                self.hazard_breakdown.get(hazard_type, 0) + 1
            )

    def record_alerts_generated(self, level: str):
        with self._metrics_lock:
            self.alerts_generated_total += 1
            if level == "HIGH":
                self.alerts_high_total += 1
            elif level == "CRITICAL":
                self.alerts_critical_total += 1

    def record_alerts_duration(self, latency_ms: float):
        with self._metrics_lock:
            self.alerts_generation_ms += latency_ms

    def record_visualization_request(self):
        with self._metrics_lock:
            self.visualization_requests_total += 1

    def record_visualization_duration(self, duration_ms: float):
        with self._metrics_lock:
            self.visualization_generation_ms += duration_ms

    def record_db_query(self, duration_ms: float, success: bool = True):
        with self._metrics_lock:
            self.db_queries_total += 1
            if success:
                self.db_query_duration_ms += duration_ms
            else:
                self.db_failures_total += 1

    def record_spatial_query(self, duration_ms: float, success: bool = True):
        with self._metrics_lock:
            self.spatial_queries_total += 1
            if success:
                self.spatial_query_duration_ms += duration_ms
            else:
                self.spatial_query_failures_total += 1

    def record_satellite_request(self, cache_hit: bool, success: bool, duration_ms: float):
        with self._metrics_lock:
            self.satellite_requests_total += 1
            if cache_hit:
                self.satellite_cache_hits_total += 1
            if not success:
                self.satellite_provider_failures_total += 1
            self.satellite_fetch_duration_ms += duration_ms

    def record_gee_request(self, cache_hit: bool, success: bool, duration_ms: float, retries: int = 0):
        with self._metrics_lock:
            self.gee_requests_total += 1
            if cache_hit:
                self.gee_cache_hits_total += 1
            if not success:
                self.gee_failures_total += 1
            self.gee_retry_total += retries
            self.gee_request_duration_ms += duration_ms

    def record_job_created(self):
        with self._metrics_lock:
            self.jobs_created_total += 1

    def record_processing_job_started(self):
        with self._metrics_lock:
            self.processing_jobs_total += 1

    def record_processing_job_completed(self, duration_ms: float):
        with self._metrics_lock:
            self.processing_duration_ms += duration_ms

    def record_processing_failure(self, duration_ms: float):
        with self._metrics_lock:
            self.processing_failures_total += 1
            self.processing_duration_ms += duration_ms

    def record_sentinel1_processed(self):
        with self._metrics_lock:
            self.sentinel1_processed_total += 1

    def record_sentinel2_processed(self):
        with self._metrics_lock:
            self.sentinel2_processed_total += 1

    def record_indices_generated(self, count: int):
        with self._metrics_lock:
            self.indices_generated_total += count

    def record_job_completed(self):
        with self._metrics_lock:
            self.jobs_completed_total += 1

    def record_job_failed(self):
        with self._metrics_lock:
            self.jobs_failed_total += 1

    def record_job_retried(self):
        with self._metrics_lock:
            self.jobs_retried_total += 1
            
    def record_deduplication_save(self):
        with self._metrics_lock:
            self.deduplication_saves_total += 1

    def record_recovered_job(self):
        with self._metrics_lock:
            self.recovered_jobs_total += 1

    def record_stale_job_requeue(self):
        with self._metrics_lock:
            self.stale_job_requeues_total += 1

    def record_idempotency_reuse(self):
        with self._metrics_lock:
            self.idempotency_reuse_total += 1
            
    def record_queue_wait(self, duration_ms: float):
        with self._metrics_lock:
            self.queue_wait_duration_ms += duration_ms

    def update_queue_depth(self, depth: int):
        with self._metrics_lock:
            self.queue_depth = depth

    def set_workers_active(self, active: int):
        with self._metrics_lock:
            self.workers_active_total = active

    def record_worker_failure(self):
        with self._metrics_lock:
            self.worker_failures_total += 1

    def record_worker_execution(self, duration_ms: float):
        with self._metrics_lock:
            self.worker_execution_duration_ms += duration_ms
            self.worker_execution_time_ms += duration_ms
            
    def update_worker_utilization(self, ratio: float):
        with self._metrics_lock:
            self.worker_utilization_ratio = ratio

    def record_processing_completed(self, duration_ms: float, is_s1: bool, is_s2: bool, indices_count: int):
        with self._metrics_lock:
            self.processing_duration_ms += duration_ms
            if is_s1:
                self.sentinel1_processed_total += 1
            if is_s2:
                self.sentinel2_processed_total += 1
            self.indices_generated_total += indices_count

    def record_baseline_cache_hit(self):
        with self._metrics_lock:
            self.baseline_cache_hits_total += 1

    def record_flood_analysis_started(self):
        with self._metrics_lock:
            self.flood_analyses_total += 1

    def record_flood_analysis_completed(self, duration_ms: float, risk_level: str):
        with self._metrics_lock:
            self.flood_detection_duration_ms += duration_ms
            self.flood_detections_total += 1
            if risk_level == "HIGH":
                self.flood_high_risk_total += 1
            elif risk_level == "CRITICAL":
                self.flood_critical_total += 1

    def record_wildfire_analysis_started(self):
        with self._metrics_lock:
            self.wildfire_analyses_total += 1

    def record_wildfire_analysis_completed(self, duration_ms: float):
        with self._metrics_lock:
            self.wildfire_processing_time_ms += duration_ms

    def record_wildfire_alert_generated(self):
        with self._metrics_lock:
            self.wildfire_alerts_generated += 1

    def record_wildfire_failure(self):
        with self._metrics_lock:
            self.wildfire_failures += 1

    def record_temporal_analysis(self, duration_ms: float):
        with self._metrics_lock:
            self.temporal_analyses_total += 1
            self.temporal_processing_duration_ms += duration_ms

    def record_temporal_failure(self):
        with self._metrics_lock:
            self.change_detection_failures += 1

    def record_temporal_cache_hit(self):
        with self._metrics_lock:
            self.temporal_cache_hits += 1

    def update_temporal_queue_depth(self, depth: int):
        with self._metrics_lock:
            self.temporal_queue_depth = depth

    def record_temporal_job_duration(self, duration_ms: float):
        with self._metrics_lock:
            self.temporal_job_duration_ms += duration_ms

    def record_temporal_scene_fetch(self, duration_ms: float):
        with self._metrics_lock:
            self.temporal_scene_fetch_duration_ms += duration_ms

    def record_temporal_geojson_size(self, size_bytes: int):
        with self._metrics_lock:
            self.temporal_geojson_size_bytes += size_bytes

    def record_intelligence_aggregation(self):
        with self._metrics_lock:
            self.intelligence_aggregations_total += 1

    def record_correlation_event(self, count: int = 1):
        with self._metrics_lock:
            self.correlation_events_total += count

    def record_explainability_generation(self, duration_ms: float):
        with self._metrics_lock:
            self.explainability_generation_ms += duration_ms

    def record_prioritization_duration(self, duration_ms: float):
        with self._metrics_lock:
            self.prioritization_duration_ms += duration_ms

    def record_intelligence_failure(self):
        with self._metrics_lock:
            self.intelligence_failures += 1

    def update_active_websocket_connections(self, count: int):
        with self._metrics_lock:
            self.active_websocket_connections = count
            
    def record_websocket_message(self, size_bytes: int, latency_ms: float = 0.0):
        with self._metrics_lock:
            self.websocket_messages_total += 1
            self.streaming_events_total += 1
            self.streaming_total_size_bytes += size_bytes
            self.streaming_latency_ms += latency_ms
            
    def record_websocket_disconnect(self, is_backpressure: bool = False):
        with self._metrics_lock:
            self.websocket_disconnects_total += 1
            if is_backpressure:
                self.websocket_backpressure_disconnects_total += 1
                
    def record_websocket_queue_overflow(self):
        with self._metrics_lock:
            self.websocket_queue_overflows_total += 1
            
    def record_pubsub_failure(self, delivery: bool = False):
        with self._metrics_lock:
            self.pubsub_failures_total += 1
            if delivery:
                self.pubsub_delivery_failures_total += 1

    # Fusion Tracking
    def record_fusion_operation(self, duration_ms: float):
        with self._metrics_lock:
            self.fusion_operations_total += 1
            self.fusion_processing_duration_ms += duration_ms

    def record_escalation_event(self):
        with self._metrics_lock:
            self.escalation_events_total += 1

    def record_anomaly_flag(self):
        with self._metrics_lock:
            self.anomaly_flags_total += 1

    def record_reliability_degradation(self):
        with self._metrics_lock:
            self.reliability_degradations_total += 1

    def record_cascading_event(self):
        with self._metrics_lock:
            self.cascading_events_detected += 1

    def record_regional_aggregation(self, duration_ms: float):
        with self._metrics_lock:
            self.regional_aggregation_duration_ms += duration_ms

    def record_federated_request(self):
        with self._metrics_lock:
            self.federated_requests_total += 1

    def record_coalesced_request(self):
        with self._metrics_lock:
            self.coalesced_requests_total += 1

    def record_provider_timeout(self):
        with self._metrics_lock:
            self.provider_timeout_total += 1

    def record_degraded_response(self):
        with self._metrics_lock:
            self.degraded_responses_total += 1

    def record_websocket_broadcast_latency(self, latency_ms: float):
        with self._metrics_lock:
            self.websocket_broadcast_latency_ms += latency_ms

    def record_tile_generation(self, duration_ms: float, tile_type: str, size_bytes: int):
        with self._metrics_lock:
            self.tile_generation_duration_ms += duration_ms
            if tile_type == "vector":
                self.vector_tiles_total += 1
                self.vector_tile_size_bytes += size_bytes
            elif tile_type == "raster":
                self.raster_tiles_total += 1
                self.raster_tile_size_bytes += size_bytes

    def record_tile_cache_hit(self):
        with self._metrics_lock:
            self.tile_cache_hits_total += 1

    def record_geometry_simplification_savings(self, savings_bytes: int):
        with self._metrics_lock:
            self.geometry_simplification_savings_bytes += savings_bytes

    def record_websocket_tile_broadcast(self):
        with self._metrics_lock:
            self.websocket_tile_broadcasts_total += 1

    def record_command_center_action(self, metric_name: str, value: float = 1.0):
        with self._metrics_lock:
            if metric_name in self.command_center_metrics:
                self.command_center_metrics[metric_name] += value
            elif metric_name in self.predictive_metrics:
                self.predictive_metrics[metric_name] += value

    def get_metrics(self) -> SystemMetricsResponse:
        with self._metrics_lock:
            avg_latency = (
                self.total_latency_ms / self.total_requests
                if self.total_requests > 0
                else 0.0
            )

            total_cache = self.cache_hits_total + self.cache_misses_total
            cache_ratio = self.cache_hits_total / total_cache if total_cache > 0 else 0.0

            avg_risk = (
                self.total_risk_score / self.total_analyses
                if self.total_analyses > 0
                else 0.0
            )

            return SystemMetricsResponse(
                api=APIMetrics(
                    total_requests=self.total_requests,
                    successful_requests=self.successful_requests,
                    failed_requests=self.failed_requests,
                    average_latency_ms=avg_latency,
                ),
                cache=CacheMetrics(
                    cache_hits_total=self.cache_hits_total,
                    cache_misses_total=self.cache_misses_total,
                    cache_hit_ratio=cache_ratio,
                    redis_lock_acquired_total=self.redis_lock_acquired_total,
                    redis_lock_wait_total_ms=self.redis_lock_wait_total_ms,
                    redis_errors_total=self.redis_errors_total,
                ),
                analysis=AnalysisMetrics(
                    total_analyses=self.total_analyses,
                    hazard_breakdown=dict(self.hazard_breakdown),
                    average_risk_score=avg_risk,
                ),
                alerts=AlertMetrics(
                    alerts_generated_total=self.alerts_generated_total,
                    alerts_high_total=self.alerts_high_total,
                    alerts_critical_total=self.alerts_critical_total,
                    alerts_generation_ms=self.alerts_generation_ms,
                ),
                visualizations=VisualizationMetrics(
                    requests_total=self.visualization_requests_total,
                    generation_ms=self.visualization_generation_ms,
                ),
                database=DatabaseMetrics(
                    queries_total=self.db_queries_total,
                    query_duration_ms=self.db_query_duration_ms,
                    failures_total=self.db_failures_total,
                ),
                spatial=SpatialMetrics(
                    spatial_queries_total=self.spatial_queries_total,
                    spatial_query_duration_ms=self.spatial_query_duration_ms,
                    spatial_query_failures_total=self.spatial_query_failures_total,
                ),
                satellite=SatelliteMetrics(
                    satellite_requests_total=self.satellite_requests_total,
                    satellite_cache_hits_total=self.satellite_cache_hits_total,
                    satellite_provider_failures_total=self.satellite_provider_failures_total,
                    satellite_fetch_duration_ms=self.satellite_fetch_duration_ms,
                ),
                gee=GEEMetrics(
                    gee_requests_total=self.gee_requests_total,
                    gee_cache_hits_total=self.gee_cache_hits_total,
                    gee_failures_total=self.gee_failures_total,
                    gee_retry_total=self.gee_retry_total,
                    gee_request_duration_ms=self.gee_request_duration_ms,
                ),
                processing=ProcessingMetrics(
                    processing_jobs_total=self.processing_jobs_total,
                    processing_failures_total=self.processing_failures_total,
                    processing_duration_ms=self.processing_duration_ms,
                    sentinel1_processed_total=self.sentinel1_processed_total,
                    sentinel2_processed_total=self.sentinel2_processed_total,
                    indices_generated_total=self.indices_generated_total,
                ),
                jobs=JobMetrics(
                    jobs_created_total=self.jobs_created_total,
                    jobs_completed_total=self.jobs_completed_total,
                    jobs_failed_total=self.jobs_failed_total,
                    jobs_cancelled_total=self.jobs_cancelled_total,
                    queue_depth=self.queue_depth,
                    deduplication_saves_total=self.deduplication_saves_total,
                    recovered_jobs_total=self.recovered_jobs_total,
                    stale_job_requeues_total=self.stale_job_requeues_total,
                    idempotency_reuse_total=self.idempotency_reuse_total,
                    queue_wait_duration_ms=self.queue_wait_duration_ms,
                ),
                workers=WorkerMetrics(
                    workers_active_total=self.workers_active_total,
                    worker_failures_total=self.worker_failures_total,
                    worker_execution_time_ms=self.worker_execution_time_ms,
                    worker_utilization_ratio=self.worker_utilization_ratio,
                ),
                flood=FloodMetrics(
                    flood_analyses_total=self.flood_analyses_total,
                    flood_detections_total=self.flood_detections_total,
                    flood_detection_duration_ms=self.flood_detection_duration_ms,
                    flood_high_risk_total=self.flood_high_risk_total,
                    flood_critical_total=self.flood_critical_total,
                    baseline_cache_hits_total=self.baseline_cache_hits_total,
                ),
                wildfire=WildfireMetrics(
                    wildfire_analyses_total=self.wildfire_analyses_total,
                    wildfire_processing_time_ms=self.wildfire_processing_time_ms,
                    wildfire_alerts_generated=self.wildfire_alerts_generated,
                    wildfire_failures=self.wildfire_failures,
                ),
                temporal=TemporalMetrics(
                    temporal_analyses_total=self.temporal_analyses_total,
                    temporal_processing_duration_ms=self.temporal_processing_duration_ms,
                    change_detection_failures=self.change_detection_failures,
                    temporal_cache_hits=self.temporal_cache_hits,
                    temporal_queue_depth=self.temporal_queue_depth,
                    temporal_job_duration_ms=self.temporal_job_duration_ms,
                    temporal_scene_fetch_duration_ms=self.temporal_scene_fetch_duration_ms,
                    temporal_geojson_size_bytes=self.temporal_geojson_size_bytes,
                ),
                intelligence=IntelligenceMetrics(
                    intelligence_aggregations_total=self.intelligence_aggregations_total,
                    correlation_events_total=self.correlation_events_total,
                    explainability_generation_ms=self.explainability_generation_ms,
                    prioritization_duration_ms=self.prioritization_duration_ms,
                    intelligence_failures=self.intelligence_failures,
                ),
                streaming=StreamingMetrics(
                    active_websocket_connections=self.active_websocket_connections,
                    websocket_messages_total=self.websocket_messages_total,
                    websocket_disconnects_total=self.websocket_disconnects_total,
                    websocket_queue_overflows_total=self.websocket_queue_overflows_total,
                    websocket_backpressure_disconnects_total=self.websocket_backpressure_disconnects_total,
                    pubsub_failures_total=self.pubsub_failures_total,
                    pubsub_delivery_failures_total=self.pubsub_delivery_failures_total,
                    streaming_latency_ms=self.streaming_latency_ms,
                    average_event_size_bytes=(self.streaming_total_size_bytes / self.streaming_events_total) if self.streaming_events_total > 0 else 0.0,
                ),
                fusion=FusionMetrics(
                    fusion_operations_total=self.fusion_operations_total,
                    escalation_events_total=self.escalation_events_total,
                    anomaly_flags_total=self.anomaly_flags_total,
                    reliability_degradations_total=self.reliability_degradations_total,
                    cascading_events_detected=self.cascading_events_detected,
                    regional_aggregation_duration_ms=self.regional_aggregation_duration_ms,
                    fusion_processing_duration_ms=self.fusion_processing_duration_ms,
                ),
                gateway=GatewayMetrics(
                    federated_requests_total=self.federated_requests_total,
                    coalesced_requests_total=self.coalesced_requests_total,
                    provider_timeout_total=self.provider_timeout_total,
                    degraded_responses_total=self.degraded_responses_total,
                    websocket_broadcast_latency_ms=self.websocket_broadcast_latency_ms,
                ),
                tiles=TileMetrics(
                    tile_generation_duration_ms=self.tile_generation_duration_ms,
                    vector_tiles_total=self.vector_tiles_total,
                    raster_tiles_total=self.raster_tiles_total,
                    vector_tile_size_bytes=self.vector_tile_size_bytes,
                    raster_tile_size_bytes=self.raster_tile_size_bytes,
                    tile_cache_hits_total=self.tile_cache_hits_total,
                    geometry_simplification_savings_bytes=self.geometry_simplification_savings_bytes,
                    websocket_tile_broadcasts_total=self.websocket_tile_broadcasts_total,
                ),
                command_center=CommandCenterMetrics(
                    **self.command_center_metrics
                ),
                predictive=PredictiveMetrics(
                    forecast_generation_total=self.predictive_metrics["forecast_generation_total"],
                    forecast_failures_total=self.predictive_metrics["forecast_failures_total"],
                    anomaly_detection_total=self.predictive_metrics["anomaly_detection_total"],
                    simulation_duration_ms=self.predictive_metrics["simulation_duration_ms"],
                    predictive_cache_hits=self.predictive_metrics["predictive_cache_hits"],
                    predictive_queue_depth=self.predictive_metrics["predictive_queue_depth"]
                ),
                infrastructure_prediction=InfrastructurePredictionMetrics(
                    infrastructure_forecast_duration_ms=self.predictive_metrics["infrastructure_forecast_duration_ms"]
                ),
                remediation=AutonomousRemediationMetrics(
                    autonomous_remediations_total=self.predictive_metrics["autonomous_remediations_total"],
                    remediation_failures_total=self.predictive_metrics["remediation_failures_total"]
                )
            )


metrics_store = MetricsStore()
