import asyncio
import logging
from typing import Any, Dict, List
from datetime import datetime

from app.gateway.federation.circuit_breaker import CircuitBreaker
from app.observability.metrics import metrics_store
from app.gateway.contracts.public import ReliabilityMetadata

logger = logging.getLogger(__name__)


class FederationEngine:
    """
    Orchestrates hazard engines concurrently with strict per-engine timeouts.
    Enforces partial degradation, ensuring a single failing engine NEVER fails the entire response.
    """

    def __init__(self):
        # We can configure specific circuit breakers per internal engine
        self.flood_breaker = CircuitBreaker("flood_engine")
        self.wildfire_breaker = CircuitBreaker("wildfire_engine")

    async def _mock_engine_call(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Replace with actual internal core logic calls
        await asyncio.sleep(0.5)
        return {"status": "ok", "engine": name, "results": []}

    async def _safe_execute(self, name: str, breaker: CircuitBreaker, payload: Dict[str, Any], timeout: float) -> Dict[str, Any]:
        async def action():
            return await asyncio.wait_for(self._mock_engine_call(name, payload), timeout=timeout)
            
        async def fallback():
            # Return degraded metadata cleanly
            return {"status": "degraded", "engine": name, "results": []}

        try:
            return await breaker.execute(action, fallback)
        except asyncio.TimeoutError:
            metrics_store.record_provider_timeout()
            logger.error(f"Engine {name} timed out after {timeout}s.")
            return await fallback()
        except Exception as e:
            logger.error(f"Engine {name} failed: {e}")
            return await fallback()

    async def orchestrate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        start_time = datetime.utcnow()
        
        # Concurrent execution with timeouts
        flood_task = asyncio.create_task(self._safe_execute("flood", self.flood_breaker, payload, timeout=2.0))
        wildfire_task = asyncio.create_task(self._safe_execute("wildfire", self.wildfire_breaker, payload, timeout=2.0))
        
        # Gather all tasks, isolating failures
        results = await asyncio.gather(flood_task, wildfire_task, return_exceptions=True)
        
        end_time = datetime.utcnow()
        latency_ms = (end_time - start_time).total_seconds() * 1000
        
        flood_res = results[0] if not isinstance(results[0], Exception) else {"status": "degraded", "engine": "flood"}
        wildfire_res = results[1] if not isinstance(results[1], Exception) else {"status": "degraded", "engine": "wildfire"}
        
        degraded_providers = []
        if flood_res.get("status") == "degraded":
            degraded_providers.append("flood")
            metrics_store.record_degraded_response()
            
        if wildfire_res.get("status") == "degraded":
            degraded_providers.append("wildfire")
            metrics_store.record_degraded_response()

        overall_confidence = 1.0 - (len(degraded_providers) * 0.2)
        
        metrics_store.record_federated_request()
        
        return {
            "flood": flood_res,
            "wildfire": wildfire_res,
            "reliability": ReliabilityMetadata(
                overall_confidence=max(0.0, overall_confidence),
                degraded_providers=degraded_providers,
                cache_hit=False,
                federation_latency_ms=latency_ms,
                data_staleness_seconds=0
            ).model_dump()
        }

federation_engine = FederationEngine()
