import pytest
from app.core.cyber.intelligence.feed import intelligence_feed

def test_intelligence_feed_deterministic():
    indicator_id = intelligence_feed.ingest_ioc("192.168.1.100", "ipv4", 0.95)
    
    assert intelligence_feed.check_ioc("192.168.1.100") is True
    assert intelligence_feed.check_ioc("10.0.0.1") is False
    assert indicator_id.startswith("ioc-")
