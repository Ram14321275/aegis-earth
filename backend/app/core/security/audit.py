import logging
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.audit import AuditLog
from app.core.security.tenants import get_current_tenant_id, get_current_user

logger = logging.getLogger(__name__)

async def log_audit_event(
    session: AsyncSession,
    action: str,
    entity_type: str,
    entity_id: str,
    details: Dict[str, Any]
) -> None:
    """
    Writes an immutable, append-only audit event.
    Automatically injects context from current tenant/user.
    """
    tenant_id = get_current_tenant_id()
    user = get_current_user()
    user_id = user.get("sub") if user else "system"
    
    # Enhance details with context
    audit_details = {
        **details,
        "user_id": user_id,
        "tenant_id": tenant_id
    }

    try:
        audit_entry = AuditLog(
            tenant_id=tenant_id or "system",
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=audit_details
        )
        session.add(audit_entry)
        await session.commit()
    except Exception as e:
        logger.error(f"Failed to write audit log: {e}")
        await session.rollback()
