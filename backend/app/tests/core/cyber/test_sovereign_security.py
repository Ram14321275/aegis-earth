import pytest
from app.core.cyber.zero_trust.fabric import zero_trust_fabric

def test_sovereign_security_boundary():
    assert zero_trust_fabric.validate_sovereign_boundary("US-EAST", "US-WEST") is True
    assert zero_trust_fabric.validate_sovereign_boundary("US-EAST", "EU-CENTRAL") is False
