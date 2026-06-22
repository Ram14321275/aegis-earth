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
    jobs_cancelled_total: int
    queue_depth: int
    deduplication_saves_total: int = 0
    recovered_jobs_total: int = 0
    stale_job_requeues_total: int = 0
    idempotency_reuse_total: int = 0
    queue_wait_duration_ms: float = 0.0

class ProcessingMetrics(BaseModel):
    processing_jobs_total: int
    processing_failures_total: int
    processing_duration_ms: float
    sentinel1_processed_total: int
    sentinel2_processed_total: int
    indices_generated_total: int

class FloodMetrics(BaseModel):
    flood_analyses_total: int
    flood_detections_total: int
    flood_detection_duration_ms: float
    flood_high_risk_total: int
    flood_critical_total: int
    baseline_cache_hits_total: int


class WildfireMetrics(BaseModel):
    wildfire_analyses_total: int
    wildfire_processing_time_ms: float
    wildfire_alerts_generated: int
    wildfire_failures: int

class TemporalMetrics(BaseModel):
    temporal_analyses_total: int
    temporal_processing_duration_ms: float
    change_detection_failures: int
    temporal_cache_hits: int
    temporal_queue_depth: int
    temporal_job_duration_ms: float
    temporal_scene_fetch_duration_ms: float
    temporal_geojson_size_bytes: int


class IntelligenceMetrics(BaseModel):
    intelligence_aggregations_total: int
    correlation_events_total: int
    explainability_generation_ms: float
    prioritization_duration_ms: float
    intelligence_failures: int


class StreamingMetrics(BaseModel):
    active_websocket_connections: int
    websocket_messages_total: int
    websocket_disconnects_total: int
    websocket_queue_overflows_total: int
    websocket_backpressure_disconnects_total: int
    pubsub_failures_total: int
    pubsub_delivery_failures_total: int
    streaming_latency_ms: float
    average_event_size_bytes: float


class WorkerMetrics(BaseModel):
    workers_active_total: int
    worker_failures_total: int
    worker_execution_time_ms: float
    worker_utilization_ratio: float = 0.0


class FusionMetrics(BaseModel):
    fusion_operations_total: int
    escalation_events_total: int
    anomaly_flags_total: int
    reliability_degradations_total: int
    cascading_events_detected: int
    regional_aggregation_duration_ms: float
    fusion_processing_duration_ms: float


class GatewayMetrics(BaseModel):
    federated_requests_total: int
    coalesced_requests_total: int
    provider_timeout_total: int
    degraded_responses_total: int
    websocket_broadcast_latency_ms: float

class TileMetrics(BaseModel):
    tile_generation_duration_ms: float
    vector_tiles_total: int
    raster_tiles_total: int
    vector_tile_size_bytes: int
    raster_tile_size_bytes: int
    tile_cache_hits_total: int
    geometry_simplification_savings_bytes: int
    websocket_tile_broadcasts_total: int

class CommandCenterMetrics(BaseModel):
    timeline_generation_duration_ms: float
    timeline_queries_total: int
    timeline_cache_hits_total: int
    hotspot_refresh_total: int
    snapshot_generation_duration_ms: float
    snapshot_persistence_duration_ms: float
    export_jobs_total: int
    export_failures_total: int
    replay_sessions_total: int
    websocket_timeline_connections: int
    command_center_active_streams: int


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
    processing: ProcessingMetrics
    jobs: JobMetrics
    workers: WorkerMetrics
    flood: FloodMetrics
    wildfire: WildfireMetrics
    temporal: TemporalMetrics
    intelligence: IntelligenceMetrics
    streaming: StreamingMetrics
    fusion: FusionMetrics
    gateway: GatewayMetrics
    tiles: TileMetrics
    command_center: CommandCenterMetrics


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
    processing: Dict[str, Any] | None = None
    flood_engine: Dict[str, Any] | None = None
