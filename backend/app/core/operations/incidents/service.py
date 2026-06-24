from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.operations.models import Incident, IncidentStatus
from app.db.models.operations import IncidentModel
from app.core.operations.incidents.repository import IncidentRepository
from app.core.operations.incidents.workflows import IncidentWorkflowEngine
from app.observability.metrics import metrics_store

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class IncidentService:
    def __init__(self, repository: IncidentRepository):
        self.repository = repository
        self.workflow_engine = IncidentWorkflowEngine()

    async def create_incident(self, session: AsyncSession, severity: str, confidence: float, title: str, description: str, linked_hazards: List[str] = None) -> Incident:
        try:
            model = await self.repository.create(session, obj_in={
                "severity": severity,
                "confidence": confidence,
                "title": title,
                "description": description,
                "linked_hazards": linked_hazards or []
            })
            metrics_store.record_command_center_action("incidents_total")
            return self._to_pydantic(model)
        except Exception as e:
            metrics_store.record_command_center_action("workflow_transition_failures")
            raise e

    async def get_incident(self, session: AsyncSession, incident_id: str) -> Optional[Incident]:
        model = await self.repository.get(session, incident_id)
        if model:
            return self._to_pydantic(model)
        return None
        
    async def update_status(self, session: AsyncSession, incident_id: str, new_status: IncidentStatus, actor_id: str) -> Incident:
        model = await self.repository.get(session, incident_id)
        if not model:
            raise ValueError("Incident not found")
            
        current_status = IncidentStatus(model.status)
        if not self.workflow_engine.validate_transition(current_status, new_status):
            metrics_store.record_command_center_action("workflow_transition_failures")
            raise ValueError(f"Invalid state transition from {current_status} to {new_status}")
            
        new_revision_number = model.revision_number + 1
        parent_revision_id = model.id
        
        model.status = new_status.value
        model.revision_number = new_revision_number
        model.parent_revision_id = parent_revision_id
        model.updated_at = utc_now()
        
        session.add(model)
        await session.commit()
        await session.refresh(model)
        
        return self._to_pydantic(model)

    def _to_pydantic(self, model: IncidentModel) -> Incident:
        return Incident(
            incident_id=model.id,
            tenant_id=model.tenant_id,
            status=IncidentStatus(model.status),
            severity=model.severity,
            confidence=model.confidence,
            title=model.title,
            description=model.description,
            assigned_analysts=model.assigned_analysts,
            linked_hazards=model.linked_hazards,
            linked_snapshots=model.linked_snapshots,
            created_at=model.created_at,
            updated_at=model.updated_at,
            revision_number=model.revision_number,
            parent_revision_id=model.parent_revision_id
        )
