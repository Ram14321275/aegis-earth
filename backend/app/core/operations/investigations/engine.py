from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.operations.models import Investigation, AnalystNote
from app.db.models.operations import InvestigationModel, AnalystNoteModel
from app.observability.metrics import metrics_store

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class InvestigationEngine:
    async def create_investigation(self, session: AsyncSession, tenant_id: str, incident_id: str, lead_analyst_id: str) -> Investigation:
        inv_id = str(uuid.uuid4())
        model = InvestigationModel(
            id=inv_id,
            tenant_id=tenant_id,
            incident_id=incident_id,
            lead_analyst_id=lead_analyst_id,
            status="ACTIVE",
            revision_number=1,
            created_at=utc_now(),
            updated_at=utc_now()
        )
        session.add(model)
        await session.commit()
        await session.refresh(model)
        metrics_store.record_command_center_action("active_investigations", 1)
        return self._to_pydantic(model)

    async def update_investigation(self, session: AsyncSession, investigation_id: str, new_summary: str, actor_id: str, new_annotations: List[Dict[str, Any]] = None) -> Investigation:
        query = select(InvestigationModel).filter(InvestigationModel.id == investigation_id)
        result = await session.execute(query)
        model = result.scalars().first()
        
        if not model:
            raise ValueError("Investigation not found")

        # Append-only immutability simulation for the active record
        new_rev = model.revision_number + 1
        parent_rev_id = model.id
        
        model.summary = new_summary
        if new_annotations is not None:
            model.annotations = new_annotations
            
        model.revision_number = new_rev
        model.parent_revision_id = parent_rev_id
        model.updated_at = utc_now()
        
        session.add(model)
        await session.commit()
        await session.refresh(model)
        
        return self._to_pydantic(model)

    async def add_analyst_note(self, session: AsyncSession, tenant_id: str, investigation_id: str, actor_id: str, content: str, evidence_links: List[str] = None) -> AnalystNote:
        note_id = str(uuid.uuid4())
        model = AnalystNoteModel(
            id=note_id,
            tenant_id=tenant_id,
            investigation_id=investigation_id,
            actor_id=actor_id,
            content=content,
            evidence_links=evidence_links or [],
            revision_number=1,
            created_at=utc_now(),
            updated_at=utc_now()
        )
        session.add(model)
        await session.commit()
        await session.refresh(model)
        return AnalystNote(
            note_id=model.id,
            tenant_id=model.tenant_id,
            investigation_id=model.investigation_id,
            actor_id=model.actor_id,
            content=model.content,
            evidence_links=model.evidence_links,
            created_at=model.created_at,
            updated_at=model.updated_at,
            revision_number=model.revision_number,
            parent_note_id=model.parent_note_id
        )

    def _to_pydantic(self, model: InvestigationModel) -> Investigation:
        return Investigation(
            investigation_id=model.id,
            tenant_id=model.tenant_id,
            incident_id=model.incident_id,
            lead_analyst_id=model.lead_analyst_id,
            status=model.status,
            summary=model.summary,
            revision_number=model.revision_number,
            parent_revision_id=model.parent_revision_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            annotations=model.annotations
        )
