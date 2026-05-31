from app.domain.alerts.models import AlertLevel


class AlertRules:
    @staticmethod
    def get_level_for_score(score: float) -> AlertLevel:
        if score <= 25.0:
            return AlertLevel.INFO
        elif score <= 50.0:
            return AlertLevel.WATCH
        elif score <= 75.0:
            return AlertLevel.WARNING
        else:
            return AlertLevel.CRITICAL
