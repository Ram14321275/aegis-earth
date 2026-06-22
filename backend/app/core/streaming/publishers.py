from app.core.streaming.models import BaseStreamEvent
from app.core.streaming.broker import streaming_broker

class EventPublisher:
    """
    Decoupled interface for internal Workers and Engines to publish events.
    Ensures workers never communicate directly with WebSocket clients.
    """
    
    @staticmethod
    async def publish(channel: str, event: BaseStreamEvent) -> bool:
        """
        Serializes the event and dispatches it onto the streaming broker.
        """
        payload = event.json()
        return await streaming_broker.publish(channel, payload)

event_publisher = EventPublisher()
