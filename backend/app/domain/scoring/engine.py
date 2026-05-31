from app.domain.models.hazard import HazardType


class RiskScoringEngine:
    @staticmethod
    def calculate_score(hazard_type: HazardType) -> float:
        scoring_map = {
            HazardType.FLOOD: 70.0,
            HazardType.WILDFIRE: 85.0,
            HazardType.VEGETATION_LOSS: 40.0,
            HazardType.URBAN_EXPANSION: 25.0,
            HazardType.UNKNOWN: 0.0,
        }
        return scoring_map.get(hazard_type, 0.0)
