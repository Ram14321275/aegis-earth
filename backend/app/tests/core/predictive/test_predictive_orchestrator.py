import pytest
from app.core.predictive.orchestration.orchestrator import predictive_orchestrator

@pytest.mark.asyncio
async def test_orchestrator_cycle():
    result = await predictive_orchestrator.run_predictive_cycle("tenant_1", "wildfire", "region_x")
    assert "forecast" in result
    assert "anomalies" in result
    assert "infrastructure" in result
    assert "remediation_plan" in result
