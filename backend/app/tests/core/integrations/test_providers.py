import pytest
import time
import asyncio
from app.core.integrations.providers.health import ProviderHealthTracker
from app.core.integrations.providers.circuit_breaker import ProviderCircuitBreaker, CircuitBreakerOpenException

def test_provider_health_tracker():
    tracker = ProviderHealthTracker()
    tracker.report_success("provider_a", 150.0)
    status = tracker.get_status("provider_a")
    assert status["status"] == "healthy"
    
    # Trigger degraded and failing
    for _ in range(2):
        tracker.report_failure("provider_a")
    assert tracker.get_status("provider_a")["status"] == "degraded"
    
    for _ in range(3):
        tracker.report_failure("provider_a")
    assert tracker.get_status("provider_a")["status"] == "failing"

@pytest.mark.asyncio
async def test_circuit_breaker():
    cb = ProviderCircuitBreaker("test_provider", max_failures=2, reset_timeout_seconds=1)
    
    async def failing_call():
        raise ValueError("Network Error")
        
    async def successful_call():
        return "success"
        
    # Initial success
    assert await cb.call(successful_call) == "success"
    
    # Trigger failures to open breaker
    with pytest.raises(ValueError):
        await cb.call(failing_call)
    with pytest.raises(ValueError):
        await cb.call(failing_call)
        
    assert cb.state == "OPEN"
    
    # Should block call
    with pytest.raises(CircuitBreakerOpenException):
        await cb.call(successful_call)
        
    # Wait for timeout to half-open
    await asyncio.sleep(1.1)
    
    # Call should succeed and close breaker
    assert await cb.call(successful_call) == "success"
    assert cb.state == "CLOSED"
