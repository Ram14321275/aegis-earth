import pytest
from app.core.cyber.quarantine.manager import quarantine_manager

def test_quarantine_flow():
    target = "service_x"
    assert quarantine_manager.is_quarantined(target) is False
    
    q_id = quarantine_manager.start_quarantine(target, "suspicious_activity")
    assert quarantine_manager.is_quarantined(target) is True
    
    quarantine_manager.lift_quarantine(target)
    assert quarantine_manager.is_quarantined(target) is False
