import time

from app.core.alerts.generators import generate_alert
from app.core.alerts.models import AlertSummary, AlertTrigger
from app.core.alerts.rules.flood import FloodAlertRule
from app.core.alerts.rules.wildfire import WildfireAlertRule
from app.core.alerts.validators import validate_alert_inputs
from app.observability.metrics import metrics_store
from app.schemas.intelligence import AnalysisResult, RiskAssessment


class AlertService:
    def __init__(self):
        self.rules = {"flood": FloodAlertRule(), "wildfire": WildfireAlertRule()}

    def generate_alerts(
        self, risk: RiskAssessment, analysis: AnalysisResult, location_meta: dict
    ) -> AlertSummary:
        start_time = time.time()
        try:
            validate_alert_inputs(risk, risk.confidence)

            hazard_type = risk.hazard_type.value.lower()
            rule = self.rules.get(hazard_type)
            if not rule:
                raise ValueError(f"No alert rule for hazard type: {hazard_type}")

            trigger = AlertTrigger(
                hazard_type=hazard_type,
                risk_level=risk.severity.value.upper(),
                risk_score=risk.score,
            )

            severity = rule.evaluate(trigger)

            reason = f"Calculated risk score is {risk.score} based on drivers: {', '.join(risk.drivers)}"

            alert = generate_alert(
                trigger=trigger,
                severity=severity,
                location=analysis.location_name,
                confidence=risk.confidence,
                reason=reason,
            )

            metrics_store.record_alerts_generated(severity.value)

            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_alerts_duration(duration_ms)

            return AlertSummary(alerts=[alert], highest_severity=severity)
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            metrics_store.record_alerts_duration(duration_ms)
            raise e

    def get_status(self) -> dict:
        return {"status": "healthy", "supported_rules": list(self.rules.keys())}


alert_service = AlertService()
