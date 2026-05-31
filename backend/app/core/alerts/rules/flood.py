from app.core.alerts.models import AlertLevel, AlertTrigger
from app.core.alerts.severity import map_risk_to_alert_level


class FloodAlertRule:
    def evaluate(self, trigger: AlertTrigger) -> AlertLevel:
        return map_risk_to_alert_level(trigger.risk_level)
