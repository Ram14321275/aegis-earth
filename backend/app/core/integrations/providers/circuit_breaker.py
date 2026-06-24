import asyncio
import time
from typing import Callable, Any
import logging
from app.core.integrations.providers.health import provider_health_tracker

logger = logging.getLogger(__name__)

class CircuitBreakerOpenException(Exception):
    pass

class ProviderCircuitBreaker:
    def __init__(self, provider_id: str, max_failures: int = 5, reset_timeout_seconds: int = 60):
        self.provider_id = provider_id
        self.max_failures = max_failures
        self.reset_timeout_seconds = reset_timeout_seconds
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN
        self.last_failure_time = 0.0
        
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.reset_timeout_seconds:
                logger.info(f"Circuit breaker for {self.provider_id} half-open.")
                self.state = "HALF-OPEN"
            else:
                raise CircuitBreakerOpenException(f"Circuit breaker is OPEN for {self.provider_id}")

        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            latency_ms = (time.time() - start_time) * 1000
            
            if self.state == "HALF-OPEN":
                logger.info(f"Circuit breaker for {self.provider_id} closed.")
                self.state = "CLOSED"
                
            provider_health_tracker.report_success(self.provider_id, latency_ms)
            return result
            
        except Exception as e:
            provider_health_tracker.report_failure(self.provider_id)
            status = provider_health_tracker.get_status(self.provider_id)
            
            if status.get("failure_count", 0) >= self.max_failures or self.state == "HALF-OPEN":
                self.state = "OPEN"
                self.last_failure_time = time.time()
                logger.error(f"Circuit breaker for {self.provider_id} OPENED due to {e}")
                
            raise
