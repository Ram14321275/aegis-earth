from datetime import datetime, timezone

from app.core.alerts.models import Alert, AlertLevel, AlertMetadata, AlertTrigger
from app.core.alerts.templates import get_template


def generate_alert(
    trigger: AlertTrigger,
    severity: AlertLevel,
    location: str,
    confidence: float,
    reason: str,
) -> Alert:
    template = get_template(trigger.hazard_type, severity.value)
    now = datetime.now(timezone.utc)

    return Alert(
        severity=severity,
        title=template["title"],
        message=template["message"],
        confidence=confidence,
        reason=reason,
        generated_at=now,
        metadata=AlertMetadata(
            location=location, confidence=confidence, generated_at=now.isoformat()
        ),
    )
