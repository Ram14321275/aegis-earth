from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any

from app.core.operations.models import TimelineEvent
from app.observability.metrics import metrics_store

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class TimelineEngine:
    def __init__(self):
        # Ephemeral storage for this implementation
        self.events: List[TimelineEvent] = []
        
    async def record_event(self, tenant_id: str, incident_id: str, actor_id: str, event_type: str, details: Dict[str, Any]) -> TimelineEvent:
        event = TimelineEvent(
            tenant_id=tenant_id,
            incident_id=incident_id,
            actor_id=actor_id,
            event_type=event_type,
            details=details,
            timestamp=utc_now()
        )
        self.events.append(event)
        return event

    async def get_timeline(self, tenant_id: str, incident_id: str) -> List[TimelineEvent]:
        # Filter and sort by timestamp
        relevant = [e for e in self.events if e.tenant_id == tenant_id and e.incident_id == incident_id]
        return sorted(relevant, key=lambda x: x.timestamp)
