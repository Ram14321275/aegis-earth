import pytest
from app.core.edge.consistency.verifier import consistency_verifier

def test_consistency_verifier():
    # Valid lineage
    events_valid = [
        {"event_id": "ev_1", "parent_event_id": "ev_0"},
        {"event_id": "ev_2", "parent_event_id": "ev_1"}
    ]
    assert consistency_verifier.verify_lineage(events_valid) is True
    
    # Invalid lineage
    events_invalid = [
        {"event_id": "ev_1", "parent_event_id": "ev_0"},
        {"event_id": "ev_3", "parent_event_id": "ev_2"} # Gap
    ]
    assert consistency_verifier.verify_lineage(events_invalid) is False
