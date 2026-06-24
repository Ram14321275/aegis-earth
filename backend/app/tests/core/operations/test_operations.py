import pytest
from datetime import datetime, timezone
import uuid

from app.core.operations.models import IncidentStatus, Incident, EscalationStatus
from app.core.operations.incidents.workflows import IncidentWorkflowEngine
from app.core.operations.escalation.engine import EscalationEngine
from app.core.operations.collaboration.sync import CollaborationSyncEngine
from app.core.operations.timeline.engine import TimelineEngine

def test_incident_workflow_transitions():
    engine = IncidentWorkflowEngine()
    
    # Valid transitions
    assert engine.validate_transition(IncidentStatus.OPEN, IncidentStatus.ACKNOWLEDGED) == True
    assert engine.validate_transition(IncidentStatus.ACKNOWLEDGED, IncidentStatus.INVESTIGATING) == True
    assert engine.validate_transition(IncidentStatus.INVESTIGATING, IncidentStatus.ESCALATED) == True
    
    # Invalid transitions
    assert engine.validate_transition(IncidentStatus.OPEN, IncidentStatus.ARCHIVED) == False
    assert engine.validate_transition(IncidentStatus.ARCHIVED, IncidentStatus.OPEN) == False

@pytest.mark.asyncio
async def test_collaboration_sync():
    engine = CollaborationSyncEngine()
    tenant_id = "tenant_1"
    room_id = "inv_123"
    
    await engine.join_room(tenant_id, room_id, "analyst_1")
    await engine.join_room(tenant_id, room_id, "analyst_2")
    
    state = engine.get_room_state(tenant_id, room_id)
    assert "analyst_1" in state["active_operators"]
    assert "analyst_2" in state["active_operators"]
    
    await engine.update_state(tenant_id, room_id, "analyst_1", {"lat": 10, "lng": 20})
    state = engine.get_room_state(tenant_id, room_id)
    assert state["states"]["analyst_1"]["state"] == {"lat": 10, "lng": 20}
    
    await engine.leave_room(tenant_id, room_id, "analyst_1")
    state = engine.get_room_state(tenant_id, room_id)
    assert "analyst_1" not in state["active_operators"]
    assert "analyst_1" not in state["states"]

@pytest.mark.asyncio
async def test_timeline_engine():
    engine = TimelineEngine()
    
    tenant_id = "tenant_1"
    incident_id = "inc_123"
    
    await engine.record_event(tenant_id, incident_id, "system", "INCIDENT_CREATED", {"severity": "HIGH"})
    await engine.record_event(tenant_id, incident_id, "analyst_1", "STATUS_CHANGED", {"new_status": "ACKNOWLEDGED"})
    
    timeline = await engine.get_timeline(tenant_id, incident_id)
    assert len(timeline) == 2
    assert timeline[0].event_type == "INCIDENT_CREATED"
    assert timeline[1].event_type == "STATUS_CHANGED"
