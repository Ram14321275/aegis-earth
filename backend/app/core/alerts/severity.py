from app.core.alerts.models import AlertLevel


def map_risk_to_alert_level(risk_level: str) -> AlertLevel:
    mapping = {
        "LOW": AlertLevel.LOW,
        "MODERATE": AlertLevel.MODERATE,
        "HIGH": AlertLevel.HIGH,
        "CRITICAL": AlertLevel.CRITICAL,
    }
    return mapping.get(risk_level.upper(), AlertLevel.LOW)
