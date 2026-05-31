import threading
from typing import Dict

from app.schemas.observability import (
    AlertMetrics,
    AnalysisMetrics,
    APIMetrics,
    CacheMetrics,
    SystemMetricsResponse,
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

        # Cache
        self.cache_hits = 0
        self.cache_misses = 0

        # Analysis
        self.total_analyses = 0
        self.hazard_breakdown: Dict[str, int] = {}
        self.total_risk_score = 0.0

        # Alerts
        self.info_alerts = 0
        self.watch_alerts = 0
        self.warning_alerts = 0
        self.critical_alerts = 0

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
                self.cache_hits += 1
            else:
                self.cache_misses += 1

    def record_analysis(self, hazard_type: str, risk_score: float):
        with self._metrics_lock:
            self.total_analyses += 1
            self.total_risk_score += risk_score
            self.hazard_breakdown[hazard_type] = (
                self.hazard_breakdown.get(hazard_type, 0) + 1
            )

    def record_alert(self, level: str):
        with self._metrics_lock:
            if level == "info":
                self.info_alerts += 1
            elif level == "watch":
                self.watch_alerts += 1
            elif level == "warning":
                self.warning_alerts += 1
            elif level == "critical":
                self.critical_alerts += 1

    def get_metrics(self) -> SystemMetricsResponse:
        with self._metrics_lock:
            avg_latency = (
                self.total_latency_ms / self.total_requests
                if self.total_requests > 0
                else 0.0
            )

            total_cache = self.cache_hits + self.cache_misses
            cache_ratio = self.cache_hits / total_cache if total_cache > 0 else 0.0

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
                    cache_hits=self.cache_hits,
                    cache_misses=self.cache_misses,
                    cache_hit_ratio=cache_ratio,
                ),
                analysis=AnalysisMetrics(
                    total_analyses=self.total_analyses,
                    hazard_breakdown=dict(self.hazard_breakdown),
                    average_risk_score=avg_risk,
                ),
                alerts=AlertMetrics(
                    info_alerts=self.info_alerts,
                    watch_alerts=self.watch_alerts,
                    warning_alerts=self.warning_alerts,
                    critical_alerts=self.critical_alerts,
                ),
            )


metrics_store = MetricsStore()
