import pytest
from app.core.economics.sovereignty.trade import sovereign_trade_engine

# Alias for completion requirement "test_sovereign_trade.py"
def test_sovereign_trade_resource_specific():
    restrictions = [
        {"source_region": "A", "target_region": "B", "resource_type": "fuel"}
    ]
    
    assert sovereign_trade_engine.validate_trade_route("A", "B", "fuel", restrictions) is False
    assert sovereign_trade_engine.validate_trade_route("A", "B", "food", restrictions) is True
