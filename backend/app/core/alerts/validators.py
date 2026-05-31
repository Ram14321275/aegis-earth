from app.schemas.intelligence import RiskAssessment


def validate_alert_inputs(risk_assessment: RiskAssessment, confidence: float):
    if confidence < 0.0 or confidence > 1.0:
        raise ValueError("Confidence must be between 0.0 and 1.0")
    if not risk_assessment.hazard_type:
        raise ValueError("Hazard type is required")
