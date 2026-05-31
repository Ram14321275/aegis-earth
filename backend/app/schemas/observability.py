from typing import Dict

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


class SystemMetricsResponse(BaseModel):
    api: APIMetrics
    cache: CacheMetrics
    analysis: AnalysisMetrics
    alerts: AlertMetrics
    visualizations: VisualizationMetrics
    database: DatabaseMetrics


class ComponentHealth(BaseModel):
    status: str
    details: Dict[str, str] = {}


class SystemHealthResponse(BaseModel):
    status: str
    components: Dict[str, ComponentHealth]
