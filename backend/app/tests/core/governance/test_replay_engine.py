import pytest
from datetime import datetime, timezone
from app.core.governance.replay.engine import ForensicReplayEngine

@pytest.mark.asyncio
async def test_replay_engine():
    engine = ForensicReplayEngine()
    ts = datetime.now(timezone.utc)
    
    state = await engine.reconstruct_state(ts, "tenant_1")
    
    assert state["tenant_id"] == "tenant_1"
    assert state["status"] == "COMPLETED"
    assert "session_id" in state
