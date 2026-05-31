from app.core.risk.models import RiskAssessmentInput


def validate_assessment_input(inputs: RiskAssessmentInput):
    if inputs.confidence_score < 0.0 or inputs.confidence_score > 1.0:
        raise ValueError("Confidence score must be between 0.0 and 1.0")
