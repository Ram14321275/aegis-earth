import pytest
from app.core.economics.lineage.tracker import resource_lineage_tracker

def test_resource_lineage_validation():
    h1 = resource_lineage_tracker.calculate_event_hash("ALLOCATION", "fuel", 100.0, "root")
    
    chain = [
        {"event_id": "1", "event_type": "ALLOCATION", "resource_type": "fuel", "amount": 100.0, "parent_hash": "root"},
        {"event_id": "2", "event_type": "TRANSFER", "resource_type": "fuel", "amount": 50.0, "parent_hash": h1}
    ]
    
    assert resource_lineage_tracker.validate_lineage(chain) is True

def test_lineage_corruption():
    chain = [
        {"event_id": "1", "event_type": "ALLOCATION", "resource_type": "fuel", "amount": 100.0, "parent_hash": "root"},
        {"event_id": "2", "event_type": "TRANSFER", "resource_type": "fuel", "amount": 50.0, "parent_hash": "invalid_hash"}
    ]
    
    assert resource_lineage_tracker.validate_lineage(chain) is False
