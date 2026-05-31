from app.domain.models.hazard import HazardDefinition, HazardType
from app.domain.scoring.engine import RiskScoringEngine
from app.providers.contracts import ProviderType
from app.schemas.intelligence import SeverityEnum


def test_hazard_definition():
    definition = HazardDefinition(
        hazard_type=HazardType.FLOOD,
        display_name="Flood",
        description="Water overflow.",
        severity_levels=[
            SeverityEnum.LOW,
            SeverityEnum.MEDIUM,
            SeverityEnum.HIGH,
            SeverityEnum.CRITICAL,
        ],
        supported_providers=[ProviderType.MOCK, ProviderType.GEE],
    )
    assert definition.hazard_type == HazardType.FLOOD
    assert len(definition.severity_levels) == 4


def test_risk_scoring_engine():
    assert RiskScoringEngine.calculate_score(HazardType.FLOOD) == 70.0
    assert RiskScoringEngine.calculate_score(HazardType.WILDFIRE) == 85.0
    assert RiskScoringEngine.calculate_score(HazardType.VEGETATION_LOSS) == 40.0
    assert RiskScoringEngine.calculate_score(HazardType.URBAN_EXPANSION) == 25.0
    assert RiskScoringEngine.calculate_score(HazardType.UNKNOWN) == 0.0
