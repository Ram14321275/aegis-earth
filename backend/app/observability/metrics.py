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
        self.workers_active_total = 0
        self.worker_failures_total = 0
        self.worker_execution_time_ms = 0.0
        self.worker_execution_duration_ms = 0.0

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
                ),
                workers=WorkerMetrics(
                    workers_active_total=self.workers_active_total,
                    worker_failures_total=self.worker_failures_total,
                    worker_execution_time_ms=self.worker_execution_time_ms,
                ),
                flood=FloodMetrics(
                    flood_analyses_total=self.flood_analyses_total,
                    flood_detections_total=self.flood_detections_total,
                    flood_detection_duration_ms=self.flood_detection_duration_ms,
                    flood_high_risk_total=self.flood_high_risk_total,
                    flood_critical_total=self.flood_critical_total,
                    baseline_cache_hits_total=self.baseline_cache_hits_total,
                ),
            )


metrics_store = MetricsStore()
