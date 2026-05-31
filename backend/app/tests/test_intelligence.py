from datetime import timezone
import pytest
from pydantic import ValidationError

from app.schemas.intelligence import (
    BaseIntelligenceModel,
    RiskAssessment,
    SeverityEnum,
    HazardTypeEnum,
)

def test_base_model_validates_confidence_range():
    # Valid
    model = BaseIntelligenceModel(
        source=["test"],
        confidence=0.5,
        severity=SeverityEnum.LOW,
        analysis_version="1.0"
    )
    assert model.confidence == 0.5
    
    # Invalid < 0
    with pytest.raises(ValidationError):
        BaseIntelligenceModel(
            source=["test"],
            confidence=-0.1,
            severity=SeverityEnum.LOW,
            analysis_version="1.0"
        )
        
    # Invalid > 1
    with pytest.raises(ValidationError):
        BaseIntelligenceModel(
            source=["test"],
            confidence=1.1,
            severity=SeverityEnum.LOW,
            analysis_version="1.0"
        )

def test_base_model_utc_timestamp_default():
    model = BaseIntelligenceModel(
        source=["test"],
        confidence=0.5,
        severity=SeverityEnum.LOW,
        analysis_version="1.0"
    )
    # Ensure it generates a UTC timezone aware datetime or we can check timezone
    assert model.generated_at.tzinfo == timezone.utc

def test_risk_assessment_score_range():
    # Valid
    risk = RiskAssessment(
        source=["test"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        hazard_type=HazardTypeEnum.FLOOD,
        score=50.0
    )
    assert risk.score == 50.0
    
    # Invalid < 0
    with pytest.raises(ValidationError):
        RiskAssessment(
            source=["test"],
            confidence=0.9,
            severity=SeverityEnum.HIGH,
            analysis_version="1.0",
            hazard_type=HazardTypeEnum.FLOOD,
            score=-1.0
        )
        
    # Invalid > 100
    with pytest.raises(ValidationError):
        RiskAssessment(
            source=["test"],
            confidence=0.9,
            severity=SeverityEnum.HIGH,
            analysis_version="1.0",
            hazard_type=HazardTypeEnum.FLOOD,
            score=100.1
        )

def test_severity_enum_validation():
    with pytest.raises(ValidationError):
        BaseIntelligenceModel(
            source=["test"],
            confidence=0.5,
            severity="extreme", # Invalid enum value
            analysis_version="1.0"
        )
