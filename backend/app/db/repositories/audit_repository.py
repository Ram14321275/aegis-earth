from app.db.models.audit import AuditLog
from app.db.repositories.base_repository import BaseRepository


class AuditRepository(BaseRepository[AuditLog]):
    pass


audit_repo = AuditRepository(AuditLog)
