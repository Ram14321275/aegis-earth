from typing import Dict

from pydantic import BaseModel


class APIMetrics(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_latency_ms: float


class CacheMetrics(BaseModel):
    cache_hits: int
    cache_misses: int
    cache_hit_ratio: float


class AnalysisMetrics(BaseModel):
    total_analyses: int
    hazard_breakdown: Dict[str, int]
    average_risk_score: float


class AlertMetrics(BaseModel):
    info_alerts: int
    watch_alerts: int
    warning_alerts: int
    critical_alerts: int


class SystemMetricsResponse(BaseModel):
    api: APIMetrics
    cache: CacheMetrics
    analysis: AnalysisMetrics
    alerts: AlertMetrics


class ComponentHealth(BaseModel):
    status: str
    details: Dict[str, str] = {}


class SystemHealthResponse(BaseModel):
    status: str
    components: Dict[str, ComponentHealth]
