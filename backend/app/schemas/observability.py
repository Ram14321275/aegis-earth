from typing import Dict, Any

from pydantic import BaseModel


class APIMetrics(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_latency_ms: float


class CacheMetrics(BaseModel):
    cache_hits_total: int
    cache_misses_total: int
    cache_hit_ratio: float
    redis_lock_acquired_total: int = 0
    redis_lock_wait_total_ms: float = 0.0
    redis_errors_total: int = 0


class AnalysisMetrics(BaseModel):
    total_analyses: int
    hazard_breakdown: Dict[str, int]
    average_risk_score: float


class AlertMetrics(BaseModel):
    alerts_generated_total: int
    alerts_high_total: int
    alerts_critical_total: int
    alerts_generation_ms: float


class VisualizationMetrics(BaseModel):
    requests_total: int
    generation_ms: float


class DatabaseMetrics(BaseModel):
    queries_total: int
    query_duration_ms: float
    failures_total: int

class SpatialMetrics(BaseModel):
    spatial_queries_total: int
    spatial_query_duration_ms: float
    spatial_query_failures_total: int

class GEEMetrics(BaseModel):
    gee_requests_total: int
    gee_cache_hits_total: int
    gee_failures_total: int
    gee_retry_total: int
    gee_request_duration_ms: float

class SatelliteMetrics(BaseModel):
    satellite_requests_total: int
    satellite_cache_hits_total: int
    satellite_provider_failures_total: int
    satellite_fetch_duration_ms: float


class JobMetrics(BaseModel):
    jobs_created_total: int
    jobs_completed_total: int
    jobs_failed_total: int
    jobs_retried_total: int
    queue_depth: int


class WorkerMetrics(BaseModel):
    workers_active_total: int
    worker_failures_total: int
    worker_execution_time_ms: float


class SystemMetricsResponse(BaseModel):
    api: APIMetrics
    cache: CacheMetrics
    analysis: AnalysisMetrics
    alerts: AlertMetrics
    visualizations: VisualizationMetrics
    database: DatabaseMetrics
    spatial: SpatialMetrics
    satellite: SatelliteMetrics
    gee: GEEMetrics
    jobs: JobMetrics
    workers: WorkerMetrics


class ComponentHealth(BaseModel):
    status: str
    details: Dict[str, str] = {}


class PostGISHealth(BaseModel):
    status: str
    version: str | None = None
    spatial_indexes: bool
    error: str | None = None


class SystemHealthResponse(BaseModel):
    status: str
    components: Dict[str, ComponentHealth]
    jobs: Dict[str, int] = {}
    workers: Dict[str, int] = {}
    postgis: PostGISHealth | None = None
    satellite: Dict[str, Any] | None = None
    gee: Dict[str, Any] | None = None
