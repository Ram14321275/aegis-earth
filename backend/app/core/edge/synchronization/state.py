from typing import Dict, Any

class SynchronizationStateMachine:
    """Manages explicit synchronization transition logic."""
    VALID_TRANSITIONS = {
        "OFFLINE": ["RECOVERING"],
        "RECOVERING": ["IN_SYNC", "DEGRADED", "OFFLINE"],
        "IN_SYNC": ["DEGRADED", "OFFLINE"],
        "DEGRADED": ["IN_SYNC", "OFFLINE"]
    }

    @staticmethod
    def can_transition(current_state: str, new_state: str) -> bool:
        if current_state not in SynchronizationStateMachine.VALID_TRANSITIONS:
            return False
        return new_state in SynchronizationStateMachine.VALID_TRANSITIONS[current_state]
