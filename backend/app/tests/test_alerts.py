import pytest

from app.core.alerts.models import AlertLevel
from app.core.alerts.service import alert_service
from app.schemas.geospatial import Coordinates
from app.schemas.intelligence import (
    AnalysisResult,
    HazardTypeEnum,
)
from app.schemas.intelligence import RiskAssessment as OldRiskAssessment
from app.schemas.intelligence import SeverityEnum


def test_alert_generation():
    risk = OldRiskAssessment(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        hazard_type=HazardTypeEnum.FLOOD,
        score=85.0,
        drivers=["driver 1"],
    )
    analysis = AnalysisResult(
        source=["mock"],
        confidence=0.9,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        location_name="Hyderabad",
        coordinates=Coordinates(lat=17.385, lon=78.4867),
        risk_assessment=risk,
        visualizations=[],
        alerts=[],
    )

    summary = alert_service.generate_alerts(risk, analysis, {})
    assert len(summary.alerts) == 1

    alert = summary.alerts[0]
    assert alert.severity == AlertLevel.HIGH
    assert alert.title == "Flood Warning"
    assert "Significant flooding risk" in alert.message
    assert alert.confidence == 0.9
    assert alert.metadata.location == "Hyderabad"


def test_invalid_confidence():
    risk = OldRiskAssessment.model_construct(
        source=["mock"],
        confidence=1.5,
        severity=SeverityEnum.HIGH,
        analysis_version="1.0",
        hazard_type=HazardTypeEnum.FLOOD,
        score=85.0,
        drivers=["driver 1"],
    )
    with pytest.raises(ValueError, match="Confidence must be between 0.0 and 1.0"):
        alert_service.generate_alerts(risk, None, {})
