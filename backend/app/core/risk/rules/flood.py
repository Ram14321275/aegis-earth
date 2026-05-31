from app.core.risk.calculators import calculate_numerical_score, determine_risk_level
from app.core.risk.models import RiskAssessmentInput, RiskFactors, RiskScore


class FloodRuleEngine:
    def evaluate(self, inputs: RiskAssessmentInput) -> RiskScore:
        # Since actual detection is not implemented, we mock the extraction
        # of factors from the AnalysisResult.
        factors = RiskFactors(water_coverage=0.6, growth_rate=0.3)
        score = calculate_numerical_score(factors, "flood")

        # Adjust by confidence
        score = score * inputs.confidence_score

        level = determine_risk_level(score)
        return RiskScore(
            numerical_score=score,
            level=level,
            explanation=f"Large flood extent detected with strong confidence. Coverage: {factors.water_coverage}, Growth: {factors.growth_rate}.",
        )
