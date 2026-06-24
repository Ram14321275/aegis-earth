import pytest
from app.core.cyber.detection.engine import detection_engine, ReasonCode

def test_threat_detection_deterministic():
    # Test valid threat
    result = detection_engine.evaluate_threat([ReasonCode.WEBSOCKET_FLOOD_PATTERN, ReasonCode.REPLAY_NONCE_REUSE])
    assert result["detected"] is True
    assert result["score"] >= 0.75
    
    # Test no threat
    result = detection_engine.evaluate_threat([])
    assert result["detected"] is False
    assert result["score"] == 0.0
    
    # Test confidence degradation
    result = detection_engine.evaluate_threat([ReasonCode.EDGE_ATTESTATION_FAILURE], staleness_seconds=1800)
    assert result["detected"] is False  # Degraded below 0.75
    assert result["confidence"] < 1.0
