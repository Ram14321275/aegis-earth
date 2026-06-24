import pytest
from app.core.governance.compliance.export import ComplianceExportEngine

@pytest.mark.asyncio
async def test_compliance_export():
    engine = ComplianceExportEngine()
    
    events = [{"id": 1}, {"id": 2}]
    bundle = await engine.generate_export("tenant_1", "auditor_1", events, "JSON")
    
    assert "manifest.json" in bundle
    assert bundle["manifest.json"]["format"] == "JSON"
    assert bundle["manifest.json"]["record_count"] == 2
    assert bundle["manifest.json"]["lineage_preserved"] is True
    
    # Invalid format
    with pytest.raises(ValueError):
        await engine.generate_export("tenant_1", "auditor_1", events, "XML")
