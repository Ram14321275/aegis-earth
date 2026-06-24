from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.db.base import get_session
from app.core.security.auth import get_current_user
from app.core.operations.incidents.repository import IncidentRepository
from app.core.operations.incidents.service import IncidentService
from app.core.operations.investigations.engine import InvestigationEngine
from app.core.operations.workflows.manager import WorkflowManager
from app.core.operations.models import Incident, Investigation, WorkflowTask, IncidentStatus

router = APIRouter()

def get_incident_service():
    repo = IncidentRepository()
    return IncidentService(repository=repo)
    
def get_investigation_engine():
    return InvestigationEngine()

def get_workflow_manager():
    return WorkflowManager()

@router.post("/incidents", response_model=Incident, status_code=status.HTTP_201_CREATED)
async def create_incident(
    severity: str,
    confidence: float,
    title: str,
    description: str,
    linked_hazards: List[str] = [],
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
    service: IncidentService = Depends(get_incident_service)
):
    incident = await service.create_incident(session, severity, confidence, title, description, linked_hazards)
    return incident

@router.get("/incidents/{incident_id}", response_model=Incident)
async def get_incident(
    incident_id: str,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
    service: IncidentService = Depends(get_incident_service)
):
    incident = await service.get_incident(session, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.patch("/incidents/{incident_id}/status", response_model=Incident)
async def update_incident_status(
    incident_id: str,
    new_status: IncidentStatus,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
    service: IncidentService = Depends(get_incident_service)
):
    try:
        actor_id = user.get("id", "unknown")
        return await service.update_status(session, incident_id, new_status, actor_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/investigations", response_model=Investigation, status_code=status.HTTP_201_CREATED)
async def create_investigation(
    incident_id: str,
    lead_analyst_id: str,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
    engine: InvestigationEngine = Depends(get_investigation_engine)
):
    tenant_id = user.get("tenant_id", "default")
    return await engine.create_investigation(session, tenant_id, incident_id, lead_analyst_id)

@router.post("/workflows", response_model=WorkflowTask, status_code=status.HTTP_201_CREATED)
async def create_workflow_task(
    mission_id: str,
    task_type: str,
    description: str,
    assignee_id: str = None,
    session: AsyncSession = Depends(get_session),
    user: dict = Depends(get_current_user),
    manager: WorkflowManager = Depends(get_workflow_manager)
):
    tenant_id = user.get("tenant_id", "default")
    return await manager.create_task(session, tenant_id, mission_id, task_type, description, assignee_id)
