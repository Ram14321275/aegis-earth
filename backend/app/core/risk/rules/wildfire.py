from app.core.risk.calculators import calculate_numerical_score, determine_risk_level
from app.core.risk.models import RiskAssessmentInput, RiskFactors, RiskScore


class WildfireRuleEngine:
    def evaluate(self, inputs: RiskAssessmentInput) -> RiskScore:
        factors = RiskFactors(burn_area=150.0, spread_rate=15.0)
        score = calculate_numerical_score(factors, "wildfire")

        score = score * inputs.confidence_score

        level = determine_risk_level(score)
        return RiskScore(
            numerical_score=score,
            level=level,
            explanation=f"Wildfire evaluated. Burn area: {factors.burn_area}, Spread rate: {factors.spread_rate}.",
        )
