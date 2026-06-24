from datetime import datetime, timezone
import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.operations.models import WorkflowTask
from app.db.models.operations import MissionWorkflowModel
from app.observability.metrics import metrics_store

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class WorkflowManager:
    async def create_task(self, session: AsyncSession, tenant_id: str, mission_id: str, task_type: str, description: str, assignee_id: str = None) -> WorkflowTask:
        task_id = str(uuid.uuid4())
        model = MissionWorkflowModel(
            id=task_id,
            tenant_id=tenant_id,
            mission_id=mission_id,
            assignee_id=assignee_id,
            status="PENDING",
            task_type=task_type,
            description=description,
            created_at=utc_now(),
            updated_at=utc_now()
        )
        
        session.add(model)
        await session.commit()
        await session.refresh(model)
        
        return WorkflowTask(
            task_id=model.id,
            tenant_id=model.tenant_id,
            mission_id=model.mission_id,
            assignee_id=model.assignee_id,
            status=model.status,
            task_type=model.task_type,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def update_task_status(self, session: AsyncSession, task_id: str, new_status: str, actor_id: str) -> WorkflowTask:
        query = select(MissionWorkflowModel).filter(MissionWorkflowModel.id == task_id)
        result = await session.execute(query)
        model = result.scalars().first()
        
        if not model:
            raise ValueError("Task not found")
            
        model.status = new_status
        model.updated_at = utc_now()
        
        session.add(model)
        await session.commit()
        await session.refresh(model)
        
        return WorkflowTask(
            task_id=model.id,
            tenant_id=model.tenant_id,
            mission_id=model.mission_id,
            assignee_id=model.assignee_id,
            status=model.status,
            task_type=model.task_type,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
