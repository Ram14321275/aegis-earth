from app.schemas.geospatial import Coordinates
from app.schemas.intelligence import (
    AnalysisResult,
    HazardTypeEnum,
    MapView,
    RiskAssessment,
    SeverityEnum,
)


class AnalysisService:
    async def analyze(
        self, location_name: str, coordinates: Coordinates
    ) -> AnalysisResult:
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
    return AnalysisService()
