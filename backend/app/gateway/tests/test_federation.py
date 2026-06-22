import asyncio
import pytest
from app.gateway.federation.circuit_breaker import CircuitBreaker, CircuitState
from app.gateway.federation.orchestrator import FederationEngine

@pytest.mark.asyncio
async def test_circuit_breaker_degradation():
    breaker = CircuitBreaker("test", failure_threshold=2, recovery_timeout_seconds=1)
    
    async def failing_action():
        raise Exception("Failure")
        
    async def fallback():
        return "fallback_result"
        
    # First failure
    assert await breaker.execute(failing_action, fallback) == "fallback_result"
    assert breaker.state == CircuitState.CLOSED
    
    # Second failure triggers OPEN
    assert await breaker.execute(failing_action, fallback) == "fallback_result"
    assert breaker.state == CircuitState.OPEN
    
    # Fast failure on OPEN
    assert await breaker.execute(failing_action, fallback) == "fallback_result"
    
    # Wait for recovery
    await asyncio.sleep(1.1)
    
    # Next call should be HALF_OPEN
    async def success_action():
        return "success"
        
    assert await breaker.execute(success_action, fallback) == "success"
    assert breaker.state == CircuitState.CLOSED


@pytest.mark.asyncio
async def test_federation_timeout_isolation():
    engine = FederationEngine()
    
    # Mock a slow engine call directly
    async def slow_call(name, payload):
        await asyncio.sleep(3.0) # Longer than 2.0s timeout
        return {"status": "ok"}
        
    engine._mock_engine_call = slow_call
    
    result = await engine.orchestrate({"test": "payload"})
    
    # Expect degradation, not a crash
    assert result["flood"]["status"] == "degraded"
    assert result["wildfire"]["status"] == "degraded"
    
    # Reliability metadata should reflect the degradation
    reliability = result["reliability"]
    assert "flood" in reliability["degraded_providers"]
    assert "wildfire" in reliability["degraded_providers"]
    assert reliability["overall_confidence"] == 0.6  # 1.0 - (2 * 0.2)
