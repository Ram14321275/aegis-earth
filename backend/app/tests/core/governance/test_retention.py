import pytest
from app.core.governance.retention.engine import RetentionEngine

@pytest.mark.asyncio
async def test_retention_engine():
    engine = RetentionEngine()
    
    # Legal hold bypasses archival
    await engine.process_retention_rules("tenant_1", active_hold=True)
    
    # Standard archival processing
    await engine.process_retention_rules("tenant_1", active_hold=False, duration_days=30)
