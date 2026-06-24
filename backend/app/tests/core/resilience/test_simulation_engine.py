import pytest
from app.core.resilience.simulation.engine import resilience_simulation_engine

@pytest.mark.asyncio
async def test_cascading_outage_simulation():
    res = await resilience_simulation_engine.run_simulation("cascading_outage", {})
    assert res["status"] == "COMPLETED"
    assert res["production_impact"] is False
    assert res["projections"]["recovery_timeline_ms"] > 0
    
@pytest.mark.asyncio
async def test_invalid_simulation():
    res = await resilience_simulation_engine.run_simulation("unknown_drill", {})
    assert res["status"] == "FAILED"
