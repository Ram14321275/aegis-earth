from typing import Dict
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class ProviderHealthTracker:
    def __init__(self):
        self._health_status: Dict[str, Dict[str, any]] = {}

    def report_success(self, provider_id: str, latency_ms: float) -> None:
        if provider_id not in self._health_status:
            self._health_status[provider_id] = {"status": "healthy", "failure_count": 0, "latency_ms": latency_ms}
        
        status = self._health_status[provider_id]
        status["failure_count"] = 0
        status["status"] = "healthy"
        # exponential moving average for latency
        status["latency_ms"] = (status["latency_ms"] * 0.8) + (latency_ms * 0.2)
        status["last_check_at"] = datetime.now(timezone.utc)

    def report_failure(self, provider_id: str) -> None:
        if provider_id not in self._health_status:
            self._health_status[provider_id] = {"status": "healthy", "failure_count": 0, "latency_ms": 0.0}
        
        status = self._health_status[provider_id]
        status["failure_count"] += 1
        
        if status["failure_count"] >= 5:
            status["status"] = "failing"
        elif status["failure_count"] >= 2:
            status["status"] = "degraded"
            
        status["last_check_at"] = datetime.now(timezone.utc)
        logger.warning(f"Provider {provider_id} failure reported. Status: {status['status']}, Failures: {status['failure_count']}")

    def get_status(self, provider_id: str) -> Dict[str, any]:
        return self._health_status.get(provider_id, {"status": "unknown"})

provider_health_tracker = ProviderHealthTracker()
