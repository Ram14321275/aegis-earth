from datetime import datetime, timezone

from app.core.visualization.models import TimelineEntry


def generate_timeline(events: list[dict]) -> list[TimelineEntry]:
    timeline = []
    for event in events:
        entry = TimelineEntry(
            timestamp=datetime.now(timezone.utc),
            event_type=event.get("type", "UNKNOWN"),
            description=event.get("description", ""),
            metadata=event.get("metadata", {}),
        )
        timeline.append(entry)
    return timeline
