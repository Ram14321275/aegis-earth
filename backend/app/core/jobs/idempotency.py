import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.job_tracking import IdempotencyRecord
from app.core.security.tenants import get_current_tenant_id

logger = logging.getLogger(__name__)

class IdempotencyManager:
    async def get_idempotency_record(self, session: AsyncSession, idempotency_key: str) -> Optional[IdempotencyRecord]:
        tenant_id = get_current_tenant_id()
        if not tenant_id:
            return None

        result = await session.execute(
            select(IdempotencyRecord).filter(
                IdempotencyRecord.idempotency_key == idempotency_key,
                IdempotencyRecord.tenant_id == tenant_id
            )
        )
        record = result.scalars().first()
        if record and record.expires_at > datetime.now(timezone.utc):
            return record
        return None

    async def create_idempotency_record(
        self, 
        session: AsyncSession, 
        idempotency_key: str, 
        job_id: str, 
        response_payload: Optional[Dict[str, Any]] = None,
        ttl_hours: int = 24
    ) -> IdempotencyRecord:
        tenant_id = get_current_tenant_id()
        if not tenant_id:
            tenant_id = "system"

        expires_at = datetime.now(timezone.utc) + timedelta(hours=ttl_hours)
        record = IdempotencyRecord(
            idempotency_key=idempotency_key,
            tenant_id=tenant_id,
            job_id=job_id,
            response_payload=response_payload,
            expires_at=expires_at
        )
        session.add(record)
        await session.flush()
        return record

idempotency_manager = IdempotencyManager()
