import pytest

from app.core.risk.models import RiskAssessmentInput
from app.core.risk.service import risk_service
from app.schemas.geospatial import Coordinates
from app.schemas.intelligence import (
    AnalysisResult,
    HazardTypeEnum,
)
from app.schemas.intelligence import RiskAssessment as OldRiskAssessment
from app.schemas.intelligence import SeverityEnum


def test_flood_risk_assessment():
    mock_risk = OldRiskAssessment(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        hazard_type=HazardTypeEnum.FLOOD,
        score=85.0,
        drivers=[],
    )
    mock_result = AnalysisResult(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        location_name="Test",
        coordinates=Coordinates(lat=0.0, lon=0.0),
        risk_assessment=mock_risk,
        visualizations=[],
        alerts=[],
    )

    inputs = RiskAssessmentInput(
        confidence_score=0.9,
        location_metadata={"region": "Test"},
        analysis_result=mock_result,
    )

    summary = risk_service.assess_risk("flood", inputs)
    assert summary.hazard_type == "flood"
    assert summary.overall_score.level in ["HIGH", "CRITICAL"]
    assert summary.confidence_score == 0.9


def test_invalid_confidence():
    mock_risk = OldRiskAssessment(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        hazard_type=HazardTypeEnum.FLOOD,
        score=85.0,
        drivers=[],
    )
    mock_result = AnalysisResult(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        location_name="Test",
        coordinates=Coordinates(lat=0.0, lon=0.0),
        risk_assessment=mock_risk,
        visualizations=[],
        alerts=[],
    )

    inputs = RiskAssessmentInput(
        confidence_score=1.5,  # Invalid
        location_metadata={"region": "Test"},
        analysis_result=mock_result,
    )

    with pytest.raises(
        ValueError, match="Confidence score must be between 0.0 and 1.0"
    ):
        risk_service.assess_risk("flood", inputs)


def test_unsupported_hazard():
    mock_risk = OldRiskAssessment(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        hazard_type=HazardTypeEnum.FLOOD,
        score=85.0,
        drivers=[],
    )
    mock_result = AnalysisResult(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        location_name="Test",
        coordinates=Coordinates(lat=0.0, lon=0.0),
        risk_assessment=mock_risk,
        visualizations=[],
        alerts=[],
    )

    inputs = RiskAssessmentInput(
        confidence_score=0.9,
        location_metadata={"region": "Test"},
        analysis_result=mock_result,
    )

    with pytest.raises(ValueError, match="Unsupported hazard type: earthquake"):
        risk_service.assess_risk("earthquake", inputs)
