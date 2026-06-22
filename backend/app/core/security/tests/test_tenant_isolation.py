import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy import select
from app.db.repositories.base_repository import BaseRepository
from app.db.base import TenantAwareModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class DummyModel(TenantAwareModel):
    __tablename__ = "dummy"
    name: Mapped[str] = mapped_column(String)

def test_base_repository_tenant_filtering():
    repo = BaseRepository(DummyModel)
    
    with patch("app.db.repositories.base_repository.get_current_tenant_id", return_value="tenant1"):
        query = repo._get_base_query()
        # The string representation of the query should contain a WHERE clause for tenant_id
        compiled = str(query.compile(compile_kwargs={"literal_binds": True}))
        assert "tenant_id = 'tenant1'" in compiled

    with patch("app.db.repositories.base_repository.get_current_tenant_id", return_value=None):
        query = repo._get_base_query()
        compiled = str(query.compile(compile_kwargs={"literal_binds": True}))
        assert "tenant_id" not in compiled # No filtering if no tenant
