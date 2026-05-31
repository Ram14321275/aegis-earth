from app.core.risk.models import RiskFactors, RiskLevel


def calculate_numerical_score(factors: RiskFactors, hazard_type: str) -> float:
    score = 0.0
    if hazard_type == "flood":
        if factors.water_coverage is not None:
            score += min(factors.water_coverage * 100, 50)
        if factors.growth_rate is not None:
            score += min(factors.growth_rate * 100, 50)
    elif hazard_type == "wildfire":
        if factors.burn_area is not None:
            score += min(factors.burn_area / 2, 50)
        if factors.spread_rate is not None:
            score += min(factors.spread_rate * 2, 50)
    return min(max(score, 0.0), 100.0)


def determine_risk_level(score: float) -> RiskLevel:
    if score >= 75:
        return RiskLevel.CRITICAL
    elif score >= 50:
        return RiskLevel.HIGH
    elif score >= 25:
        return RiskLevel.MODERATE
    return RiskLevel.LOW
