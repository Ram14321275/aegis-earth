import pytest
from app.core.streaming.models import ClientSubscription, FloodEvent, StreamEventType
from app.domain.models.hazard import HazardType
from app.schemas.intelligence import SeverityEnum
from app.core.streaming.subscriptions import SubscriptionManager

def test_subscription_filtering():
    manager = SubscriptionManager()
    
    # Client only wants CRITICAL events from region XYZ
    sub = ClientSubscription(
        regions=["XYZ"],
        min_severity=SeverityEnum.CRITICAL
    )
    manager.set_subscription("conn_1", sub)
    
    # High severity event (Should fail severity check)
    event_high = FloodEvent(
        source="engine",
        severity=SeverityEnum.HIGH,
        location_id="XYZ",
        affected_area_km2=10.0
    )
    assert manager.should_dispatch("conn_1", event_high) == False
    
    # Critical event wrong region (Should fail region check)
    event_wrong_region = FloodEvent(
        source="engine",
        severity=SeverityEnum.CRITICAL,
        location_id="ABC",
        affected_area_km2=10.0
    )
    assert manager.should_dispatch("conn_1", event_wrong_region) == False
    
    # Critical event correct region (Should pass)
    event_correct = FloodEvent(
        source="engine",
        severity=SeverityEnum.CRITICAL,
        location_id="XYZ",
        affected_area_km2=10.0
    )
    assert manager.should_dispatch("conn_1", event_correct) == True
