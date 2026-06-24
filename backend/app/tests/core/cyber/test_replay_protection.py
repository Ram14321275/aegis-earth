import pytest
from app.core.cyber.zero_trust.fabric import zero_trust_fabric

def test_replay_protection():
    zero_trust_fabric._nonce_cache.clear()
    assert zero_trust_fabric.validate_request_lineage("n_1", "n_abc", 10) is True
    assert zero_trust_fabric.validate_request_lineage("n_1", "n_abc", 11) is False
