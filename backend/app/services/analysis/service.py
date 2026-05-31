from fastapi import Depends

from app.core.config import get_settings
from app.schemas.geospatial import Coordinates
from app.schemas.intelligence import (
    AlertResponse,
    AnalysisResult,
    DifferenceMapView,
    HeatMapView,
    MapView,
    RiskAssessment,
    HazardTypeEnum,
    SeverityEnum,
)
from app.providers.base import ProviderInterface
from app.providers.contracts import ProviderConfig, ProviderType
from app.providers.manager import ProviderManager


class AnalysisService:
    def __init__(self, provider: ProviderInterface):
        self.provider = provider

    async def analyze(
        self, location_name: str, coordinates: Coordinates
    ) -> AnalysisResult:
        # Fetch imagery and metadata via provider
        imagery = await self.provider.get_imagery(coordinates.lat, coordinates.lon)
        metadata = await self.provider.get_metadata(coordinates.lat, coordinates.lon)
        """
        Mock implementation of the disaster analysis engine.
        Returns a mocked AnalysisResult.
        """
        risk = RiskAssessment(
            source=["Aegis Mock Engine"],
            confidence=0.85,
            severity=SeverityEnum.MEDIUM,
            analysis_version="1.0.0-mock",
            hazard_type=HazardTypeEnum.FLOOD,
            score=65.0,
            drivers=["High precipitation forecast", "Low elevation"],
        )

        map_view = MapView(
            source=["Aegis Mock Engine"],
            confidence=0.9,
            severity=SeverityEnum.LOW,
            analysis_version="1.0.0-mock",
            layer_url="https://mock.tiles.aegis.earth/flood/{z}/{x}/{y}.png",
            bounds=[
                coordinates.lon - 0.1,
                coordinates.lat - 0.1,
                coordinates.lon + 0.1,
                coordinates.lat + 0.1,
            ],
        )

        return AnalysisResult(
            source=["Aegis Mock Engine"],
            confidence=0.85,
            severity=SeverityEnum.MEDIUM,
            analysis_version="1.0.0-mock",
            location_name=location_name,
            coordinates=coordinates,
            risk_assessment=risk,
            visualizations=[map_view],
            alerts=[],
        )


def get_analysis_service() -> AnalysisService:
    settings = get_settings()
    provider_type = ProviderType(settings.active_provider)
    config = ProviderConfig(provider_type=provider_type)
    provider = ProviderManager.get_provider(config)
    return AnalysisService(provider)
