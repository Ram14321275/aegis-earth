import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from app.core.copilot.orchestration.orchestrator import CopilotOrchestrator
from app.core.copilot.models import CopilotResponse, MissionContext
from app.core.security.tenants import get_current_tenant_id

router = APIRouter(prefix="/copilot", tags=["Copilot & Mission Intelligence"])
orchestrator = CopilotOrchestrator()


def get_tenant_id() -> str:
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        return "system"
    return tenant_id


@router.get("/summary", response_model=CopilotResponse)
async def get_copilot_summary(tenant_id: str = Depends(get_tenant_id)):
    context = MissionContext(
        mission_id=f"mission-{uuid.uuid4().hex[:6]}",
        tenant_id=tenant_id,
        region_id="Global",
        infrastructure_status="OPERATIONAL"
    )
    return await orchestrator.generate_mission_intelligence(
        tenant_id, context.mission_id, context, [], []
    )


@router.get("/mission/{mission_id}", response_model=CopilotResponse)
async def get_mission_intelligence(mission_id: str, tenant_id: str = Depends(get_tenant_id)):
    context = MissionContext(
        mission_id=mission_id,
        tenant_id=tenant_id,
        infrastructure_status="OPERATIONAL"
    )
    return await orchestrator.generate_mission_intelligence(
        tenant_id, mission_id, context, [], []
    )


@router.get("/recommendations", response_model=CopilotResponse)
async def get_copilot_recommendations(tenant_id: str = Depends(get_tenant_id)):
    context = MissionContext(
        mission_id=f"mission-recs-{uuid.uuid4().hex[:6]}",
        tenant_id=tenant_id,
        infrastructure_status="OPERATIONAL"
    )
    return await orchestrator.generate_mission_intelligence(
        tenant_id, context.mission_id, context, [], []
    )


@router.get("/escalations", response_model=CopilotResponse)
async def get_copilot_escalations(tenant_id: str = Depends(get_tenant_id)):
    context = MissionContext(
        mission_id=f"mission-esc-{uuid.uuid4().hex[:6]}",
        tenant_id=tenant_id,
        infrastructure_status="OPERATIONAL"
    )
    return await orchestrator.generate_mission_intelligence(
        tenant_id, context.mission_id, context, [], []
    )
