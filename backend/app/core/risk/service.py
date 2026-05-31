from app.core.risk.models import RiskAssessmentInput, RiskSummary
from app.core.risk.rules.flood import FloodRuleEngine
from app.core.risk.rules.wildfire import WildfireRuleEngine
from app.core.risk.validators import validate_assessment_input


class RiskAssessmentService:
    def __init__(self):
        self.flood_engine = FloodRuleEngine()
        self.wildfire_engine = WildfireRuleEngine()

    def assess_risk(
        self, hazard_type: str, inputs: RiskAssessmentInput
    ) -> RiskSummary:
        validate_assessment_input(inputs)

        if hazard_type == "flood":
            score = self.flood_engine.evaluate(inputs)
        elif hazard_type == "wildfire":
            score = self.wildfire_engine.evaluate(inputs)
        else:
            raise ValueError(f"Unsupported hazard type: {hazard_type}")

        return RiskSummary(
            hazard_type=hazard_type,
            overall_score=score,
            contributing_factors=[score.explanation],
            confidence_score=inputs.confidence_score,
        )


risk_service = RiskAssessmentService()
