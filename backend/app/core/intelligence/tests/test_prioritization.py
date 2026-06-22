import pytest
from datetime import datetime
from app.core.intelligence.models import IntelligenceSignal, SignalSource
from app.domain.models.hazard import HazardType
from app.schemas.intelligence import SeverityEnum
from app.core.intelligence.prioritization import event_prioritization_engine

def test_prioritization_engine():
    signals = [
        IntelligenceSignal(
            signal_id="low_sev", source=SignalSource.FLOOD_ENGINE, hazard_type=HazardType.FLOOD,
            severity=SeverityEnum.LOW, confidence=0.5, affected_area_km2=1.0, detected_at=datetime.utcnow(), raw_score=20.0
        ),
        IntelligenceSignal(
            signal_id="crit_sev", source=SignalSource.WILDFIRE_ENGINE, hazard_type=HazardType.WILDFIRE,
            severity=SeverityEnum.CRITICAL, confidence=0.9, affected_area_km2=500.0, detected_at=datetime.utcnow(), raw_score=95.0
        ),
        IntelligenceSignal(
            signal_id="med_sev", source=SignalSource.CHANGE_DETECTION_ENGINE, hazard_type=HazardType.VEGETATION_LOSS,
            severity=SeverityEnum.MEDIUM, confidence=0.8, affected_area_km2=10.0, detected_at=datetime.utcnow(), raw_score=60.0
        )
    ]
    
    prioritized = event_prioritization_engine.prioritize(signals)
    
    assert len(prioritized) == 3
    assert prioritized[0].signal.signal_id == "crit_sev"
    assert prioritized[1].signal.signal_id == "med_sev"
    assert prioritized[2].signal.signal_id == "low_sev"
    
    assert prioritized[0].priority_rank == 1
    assert prioritized[1].priority_rank == 2
    assert prioritized[2].priority_rank == 3
