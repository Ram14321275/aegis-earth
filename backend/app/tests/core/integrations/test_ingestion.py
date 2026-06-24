import pytest
from app.core.integrations.ingestion.pipeline import IngestionPipeline, PayloadValidator

@pytest.mark.asyncio
async def test_ingestion_pipeline():
    pipeline = IngestionPipeline()
    
    # Valid payload
    payload1 = {"type": "wildfire", "severity": "high", "location": "california"}
    success, msg = await pipeline.process_payload("provider_1", payload1)
    assert success is True
    
    # Duplicate payload
    success, msg = await pipeline.process_payload("provider_1", payload1)
    assert success is True
    assert msg == "Duplicate dropped"
    
    # Invalid payload (schema failure)
    success, msg = await pipeline.process_payload("provider_1", []) # list instead of dict
    assert success is False
    assert "Quarantined" in msg

def test_payload_validator_hash():
    payload1 = {"a": 1, "b": 2}
    payload2 = {"b": 2, "a": 1} # Different order, should have same hash
    
    hash1 = PayloadValidator.generate_hash(payload1)
    hash2 = PayloadValidator.generate_hash(payload2)
    assert hash1 == hash2
