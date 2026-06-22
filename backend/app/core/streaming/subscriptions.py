import logging
from typing import Dict

from app.core.streaming.models import ClientSubscription, BaseStreamEvent
from app.schemas.intelligence import SeverityEnum

logger = logging.getLogger(__name__)

class SubscriptionManager:
    """
    Handles dynamic subscription filtering for WebSocket clients.
    Evaluates whether a specific event should be dispatched to a client based on their subscription configuration.
    """
    
    def __init__(self):
        # Maps connection_id to ClientSubscription
        self._subscriptions: Dict[str, ClientSubscription] = {}
        
    def set_subscription(self, connection_id: str, sub: ClientSubscription):
        self._subscriptions[connection_id] = sub
        
    def get_subscription(self, connection_id: str) -> ClientSubscription:
        # Default empty subscription if none set (receives nothing)
        return self._subscriptions.get(connection_id, ClientSubscription())
        
    def remove_subscription(self, connection_id: str):
        self._subscriptions.pop(connection_id, None)

    @staticmethod
    def _severity_to_int(severity: SeverityEnum) -> int:
        mapping = {
            SeverityEnum.LOW: 1,
            SeverityEnum.MEDIUM: 2,
            SeverityEnum.HIGH: 3,
            SeverityEnum.CRITICAL: 4
        }
        return mapping.get(severity, 0)

    def should_dispatch(self, connection_id: str, event: BaseStreamEvent) -> bool:
        """
        Evaluates the event against the client's subscription rules.
        """
        sub = self.get_subscription(connection_id)
        
        # If client requested specific categories and this event type isn't in it, drop.
        if sub.intelligence_categories and event.event_type not in sub.intelligence_categories:
            return False
            
        # If client requested specific hazard types and this event has a hazard type not in it, drop.
        if sub.hazard_types and event.hazard_type and event.hazard_type not in sub.hazard_types:
            return False
            
        # Region filtering
        if sub.regions and event.location_id and event.location_id not in sub.regions:
            return False
            
        # Severity filtering (only dispatch if severity >= min_severity)
        if sub.min_severity and event.severity:
            event_sev = self._severity_to_int(event.severity)
            min_sev = self._severity_to_int(sub.min_severity)
            if event_sev < min_sev:
                return False
                
        return True

subscription_manager = SubscriptionManager()
