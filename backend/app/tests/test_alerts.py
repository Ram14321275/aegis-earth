from app.domain.alerts.engine import AlertEngine
from app.domain.alerts.models import AlertLevel
from app.domain.alerts.rules import AlertRules
from app.domain.models.hazard import HazardType


def test_alert_rules():
    assert AlertRules.get_level_for_score(0) == AlertLevel.INFO
    assert AlertRules.get_level_for_score(25) == AlertLevel.INFO
    assert AlertRules.get_level_for_score(26) == AlertLevel.WATCH
    assert AlertRules.get_level_for_score(50) == AlertLevel.WATCH
    assert AlertRules.get_level_for_score(51) == AlertLevel.WARNING
    assert AlertRules.get_level_for_score(75) == AlertLevel.WARNING
    assert AlertRules.get_level_for_score(76) == AlertLevel.CRITICAL
    assert AlertRules.get_level_for_score(100) == AlertLevel.CRITICAL


def test_alert_engine():
    alert = AlertEngine.generate_alert(HazardType.FLOOD, 85.0)
    assert alert.title == "Flood Alert"
    assert alert.level == AlertLevel.CRITICAL
    assert "Extreme hazard" in alert.description

    alert2 = AlertEngine.generate_alert(HazardType.WILDFIRE, 40.0)
    assert alert2.title == "Wildfire Alert"
    assert alert2.level == AlertLevel.WATCH
