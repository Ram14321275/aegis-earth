import pytest
from app.core.economics.markets.engine import market_signal_engine

def test_market_signal_ingestion():
    res = market_signal_engine.ingest_signal("COMMODITY_SPIKE", volatility=0.9, staleness_seconds=3000)
    assert res["type"] == "COMMODITY_SPIKE"
    # confidence = 1.0 - (3000 / 6000) = 0.5
    assert res["confidence_score"] == 0.5
    assert "reasoning_hash" in res
