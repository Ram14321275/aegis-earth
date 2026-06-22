import pytest
from datetime import datetime
from app.core.intelligence.models import IntelligenceSignal, SignalSource
from app.domain.models.hazard import HazardType
from app.schemas.intelligence import SeverityEnum
from app.core.intelligence.orchestrator import unified_intelligence_orchestrator

@pytest.mark.anyio
async def test_orchestrator_aggregation():
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
    
    assessment = await unified_intelligence_orchestrator.aggregate(signals)
    
    assert assessment.assessment_id.startswith("intel_")
    assert len(assessment.signals) == 2
    assert len(assessment.correlations) == 1
    assert assessment.correlations[0].relationship_type == "causes"
    assert len(assessment.prioritized_events) == 2
    assert len(assessment.explainability.contributing_indicators) == 2
