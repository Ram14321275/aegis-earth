from datetime import datetime, timezone, timedelta
from typing import Optional, List
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.operations.models import EscalationEvent, EscalationStatus
from app.db.models.operations import EscalationEventModel
from app.observability.metrics import metrics_store

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class EscalationEngine:
    COOLDOWN_MINUTES = 15
    MAX_DEPTH = 3

    async def route_escalation(self, session: AsyncSession, tenant_id: str, incident_id: str, source_system: str, severity: str, reasoning: str, correlation_id: str) -> Optional[EscalationEvent]:
        # Duplicate/Cooldown Suppression Check
        query = select(EscalationEventModel).filter(
            EscalationEventModel.incident_id == incident_id,
            EscalationEventModel.source_system == source_system,
            EscalationEventModel.status == "PENDING"
        ).order_by(EscalationEventModel.created_at.desc()).limit(self.MAX_DEPTH)
        
        result = await session.execute(query)
        recent_escalations = list(result.scalars().all())

        if len(recent_escalations) >= self.MAX_DEPTH:
            return None # Reached max escalation depth for pending items

        if recent_escalations:
            latest = recent_escalations[0]
            if utc_now() < latest.cooldown_expires_at:
                return None # Still in cooldown

        esc_id = str(uuid.uuid4())
        cooldown_expiry = utc_now() + timedelta(minutes=self.COOLDOWN_MINUTES)
        
        model = EscalationEventModel(
            id=esc_id,
            tenant_id=tenant_id,
            incident_id=incident_id,
            source_system=source_system,
            severity=severity,
            status="PENDING",
            cooldown_expires_at=cooldown_expiry,
            correlation_id=correlation_id,
            reasoning=reasoning,
            created_at=utc_now()
        )
        
        session.add(model)
        await session.commit()
        await session.refresh(model)
        
        metrics_store.record_command_center_action("escalation_events_total", 1)
        
        return EscalationEvent(
            escalation_id=model.id,
            tenant_id=model.tenant_id,
            incident_id=model.incident_id,
            source_system=model.source_system,
            severity=model.severity,
            status=EscalationStatus(model.status),
            cooldown_expires_at=model.cooldown_expires_at,
            correlation_id=model.correlation_id,
            reasoning=model.reasoning,
            created_at=model.created_at
        )

    async def acknowledge_escalation(self, session: AsyncSession, escalation_id: str, actor_id: str) -> EscalationEvent:
        query = select(EscalationEventModel).filter(EscalationEventModel.id == escalation_id)
        result = await session.execute(query)
        model = result.scalars().first()
        
        if not model:
            raise ValueError("Escalation not found")
            
        model.status = EscalationStatus.ACKNOWLEDGED.value
        model.acknowledged_by = actor_id
        model.acknowledged_at = utc_now()
        
        session.add(model)
        await session.commit()
        await session.refresh(model)
        
        return EscalationEvent(
            escalation_id=model.id,
            tenant_id=model.tenant_id,
            incident_id=model.incident_id,
            source_system=model.source_system,
            severity=model.severity,
            status=EscalationStatus(model.status),
            cooldown_expires_at=model.cooldown_expires_at,
            correlation_id=model.correlation_id,
            reasoning=model.reasoning,
            created_at=model.created_at,
            acknowledged_by=model.acknowledged_by,
            acknowledged_at=model.acknowledged_at
        )
