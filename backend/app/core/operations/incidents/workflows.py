from app.core.operations.models import IncidentStatus

class IncidentWorkflowEngine:
    @staticmethod
    def validate_transition(current_status: IncidentStatus, new_status: IncidentStatus) -> bool:
        """
        Validates whether a transition between states is allowed.
        """
        if current_status == new_status:
            return True
            
        allowed_transitions = {
            IncidentStatus.OPEN: [IncidentStatus.ACKNOWLEDGED, IncidentStatus.INVESTIGATING, IncidentStatus.RESOLVED],
            IncidentStatus.ACKNOWLEDGED: [IncidentStatus.INVESTIGATING, IncidentStatus.ESCALATED, IncidentStatus.RESOLVED],
            IncidentStatus.INVESTIGATING: [IncidentStatus.ESCALATED, IncidentStatus.RESOLVED],
            IncidentStatus.ESCALATED: [IncidentStatus.INVESTIGATING, IncidentStatus.RESOLVED],
            IncidentStatus.RESOLVED: [IncidentStatus.ARCHIVED, IncidentStatus.INVESTIGATING],
            IncidentStatus.ARCHIVED: []
        }
        
        return new_status in allowed_transitions.get(current_status, [])
