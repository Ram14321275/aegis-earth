import pytest
from datetime import datetime
from app.core.intelligence.models import IntelligenceSignal, SignalSource
from app.domain.models.hazard import HazardType
from app.schemas.intelligence import SeverityEnum
from app.core.intelligence.correlation import cross_hazard_correlation_engine

def test_correlate_wildfire_to_vegetation():
    signals = [
        IntelligenceSignal(
            signal_id="w1", source=SignalSource.WILDFIRE_ENGINE, hazard_type=HazardType.WILDFIRE,
            severity=SeverityEnum.HIGH, confidence=0.9, affected_area_km2=10.0, detected_at=datetime.utcnow(), raw_score=80.0
        ),
        IntelligenceSignal(
            signal_id="v1", source=SignalSource.CHANGE_DETECTION_ENGINE, hazard_type=HazardType.VEGETATION_LOSS,
            severity=SeverityEnum.MEDIUM, confidence=0.8, affected_area_km2=5.0, detected_at=datetime.utcnow(), raw_score=60.0
        )
    ]
    correlations = cross_hazard_correlation_engine.correlate(signals)
    assert len(correlations) == 1
    assert correlations[0].primary_signal_id == "w1"
    assert correlations[0].secondary_signal_id == "v1"
    assert correlations[0].relationship_type == "causes"

def test_correlate_vegetation_to_flood():
    signals = [
        IntelligenceSignal(
            signal_id="v1", source=SignalSource.CHANGE_DETECTION_ENGINE, hazard_type=HazardType.VEGETATION_LOSS,
            severity=SeverityEnum.HIGH, confidence=0.9, affected_area_km2=10.0, detected_at=datetime.utcnow(), raw_score=80.0
        ),
        IntelligenceSignal(
            signal_id="f1", source=SignalSource.FLOOD_ENGINE, hazard_type=HazardType.FLOOD,
            severity=SeverityEnum.HIGH, confidence=0.8, affected_area_km2=5.0, detected_at=datetime.utcnow(), raw_score=60.0
        )
    ]
    correlations = cross_hazard_correlation_engine.correlate(signals)
    assert len(correlations) == 1
    assert correlations[0].primary_signal_id == "v1"
    assert correlations[0].secondary_signal_id == "f1"
    assert correlations[0].relationship_type == "amplifies"
