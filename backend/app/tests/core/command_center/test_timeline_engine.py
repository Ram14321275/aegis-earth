import pytest
from app.core.command_center.timeline.engine import global_timeline_engine

@pytest.mark.asyncio
async def test_timeline_engine_generation():
    # Test generation for 24h
    summary = await global_timeline_engine.generate_timeline("tenant1", "24h", force_dynamic=True)
    assert summary.global_threat_level is not None
    assert len(summary.critical_regions) > 0
    assert summary.critical_regions[0].active_hotspots[0].threat_score > 0
