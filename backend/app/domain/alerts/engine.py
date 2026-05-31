from app.domain.alerts.models import Alert, AlertLevel
from app.domain.alerts.rules import AlertRules
from app.domain.models.hazard import HazardType


class AlertEngine:
    @staticmethod
    def generate_alert(hazard_type: HazardType, score: float) -> Alert:
        level = AlertRules.get_level_for_score(score)

        title = f"{hazard_type.value.replace('_', ' ').title()} Alert"

        description_map = {
            AlertLevel.INFO: "Conditions are normal, but monitor local updates.",
            AlertLevel.WATCH: "Conditions are developing. Be prepared.",
            AlertLevel.WARNING: "Hazard is imminent or occurring. Take action.",
            AlertLevel.CRITICAL: "Extreme hazard! Immediate action required to protect life and property.",
        }

        recommendation_map = {
            AlertLevel.INFO: "No immediate action required.",
            AlertLevel.WATCH: "Review emergency plans and stay informed.",
            AlertLevel.WARNING: "Execute emergency plans and follow local authority guidance.",
            AlertLevel.CRITICAL: "Evacuate immediately if ordered. Follow all emergency instructions.",
        }

        return Alert(
            title=title,
            description=description_map[level],
            recommendation=recommendation_map[level],
            level=level,
        )
