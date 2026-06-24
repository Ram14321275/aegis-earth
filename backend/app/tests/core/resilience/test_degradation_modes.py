import pytest
from app.core.resilience.degradation.modes import degradation_manager

def test_degradation_modes():
    assert degradation_manager.transition_mode("READ_ONLY") is True
    assert degradation_manager.get_current_mode() == "READ_ONLY"
    
    assert degradation_manager.transition_mode("INVALID_MODE") is False
    assert degradation_manager.get_current_mode() == "READ_ONLY"
