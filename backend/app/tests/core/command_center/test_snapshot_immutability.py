import pytest
from app.core.command_center.snapshots.engine import snapshot_engine
from app.schemas.command_center import GlobalThreatSummary
from datetime import datetime

@pytest.mark.asyncio
async def test_snapshot_creation_and_retrieval():
    mock_summary = GlobalThreatSummary(
        timestamp=datetime.utcnow(),
        global_threat_level="ELEVATED",
        critical_regions=[],
        global_insights=[]
    )
    
    # Create
    snapshot = await snapshot_engine.create_snapshot("tenant1", "24h", mock_summary)
    assert snapshot.snapshot_id is not None
    assert snapshot.revision_number == 1
    
    # Create child (revision)
    snapshot2 = await snapshot_engine.create_snapshot("tenant1", "24h", mock_summary, parent_snapshot_id=snapshot.snapshot_id)
    assert snapshot2.revision_number == 2
    assert snapshot2.parent_snapshot_id == snapshot.snapshot_id
