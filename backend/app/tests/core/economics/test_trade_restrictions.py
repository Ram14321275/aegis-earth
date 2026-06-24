import pytest
from app.core.economics.sovereignty.trade import sovereign_trade_engine

def test_trade_restrictions_enforcement():
    restrictions = [
        {"source_region": "US-EAST", "target_region": "RESTRICTED-ZONE", "resource_type": "ALL"}
    ]
    
    # Blocked route
    valid = sovereign_trade_engine.validate_trade_route("US-EAST", "RESTRICTED-ZONE", "energy", restrictions)
    assert valid is False
    
    # Allowed route
    valid2 = sovereign_trade_engine.validate_trade_route("US-EAST", "EU-WEST", "energy", restrictions)
    assert valid2 is True
