import pytest
from datetime import datetime, timezone
from app.core.governance.replay.engine import ForensicReplayEngine

@pytest.mark.asyncio
async def test_forensic_reconstruction():
    engine = ForensicReplayEngine()
    
    ts = datetime.now(timezone.utc)
    state = await engine.reconstruct_state(ts, "tenant_test")
    
    # Must be deterministic and contain expected fields
    assert state["status"] == "COMPLETED"
    assert state["tenant_id"] == "tenant_test"
    assert "reconstructed_entities" in state
    assert "active_alerts" in state["reconstructed_entities"]
