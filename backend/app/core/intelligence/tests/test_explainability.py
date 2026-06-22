import pytest
from datetime import datetime
from app.core.intelligence.models import IntelligenceSignal, SignalSource, CorrelatedHazard
from app.domain.models.hazard import HazardType
from app.schemas.intelligence import SeverityEnum
from app.core.intelligence.explainability import explainability_engine

@pytest.mark.anyio
async def test_explainability_generation():
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
    correlations = [
        CorrelatedHazard(
            primary_signal_id="w1",
            secondary_signal_id="v1",
            relationship_type="causes",
            correlation_confidence=0.8,
            description="Active wildfire is directly causing detected vegetation loss / burn scars."
        )
    ]
    
    explanation = await explainability_engine.generate(signals, correlations)
    
    assert "wildfire" in explanation.contributing_indicators
    assert "vegetation_loss" in explanation.contributing_indicators
    assert "cascading environmental risks" in explanation.reasoning_summary
    assert len(explanation.detected_environmental_changes) == 1
