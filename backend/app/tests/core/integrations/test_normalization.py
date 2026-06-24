import pytest
from app.core.integrations.normalization.engine import NormalizationEngine

def test_normalization_engine():
    engine = NormalizationEngine()
    
    payload = {
        "type": "earthquake",
        "severity": "extreme",
        "confidence": 0.95,
        "coordinates": {
            "lat": 34.05,
            "lon": -118.25
        }
    }
    
    event = engine.normalize("usgs", "eq-123", payload)
    
    assert event is not None
    assert event.event_type == "EARTHQUAKE"
    assert event.severity.level == "CRITICAL"
    assert event.severity.score == 0.9
    assert event.confidence == 0.95 * 0.9 # Adjusted confidence
    assert event.latitude == 34.05
    assert event.longitude == -118.25
    assert event.provider_source == "usgs"
    assert event.original_event_id == "eq-123"
