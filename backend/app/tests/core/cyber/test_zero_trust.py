import pytest
from app.core.cyber.zero_trust.fabric import zero_trust_fabric

def test_zero_trust_lineage_and_replay():
    # Fresh request
    assert zero_trust_fabric.validate_request_lineage("node_1", "nonce_1", 1) is True
    
    # Replay nonce
    assert zero_trust_fabric.validate_request_lineage("node_1", "nonce_1", 2) is False
    
    # Valid next counter
    assert zero_trust_fabric.validate_request_lineage("node_1", "nonce_2", 2) is True
    
    # Invalid old counter (monotonic failure)
    assert zero_trust_fabric.validate_request_lineage("node_1", "nonce_3", 1) is False
