import time
from typing import Any, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base
from app.observability.metrics import metrics_store

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        start = time.time()
        try:
            result = await session.execute(
                select(self.model).filter(self.model.id == id)
            )
            obj = result.scalars().first()

            duration = (time.time() - start) * 1000
            metrics_store.record_db_query(duration, True)
            return obj
        except Exception as e:
            metrics_store.record_db_query(0, False)
            raise e

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        start = time.time()
        try:
            result = await session.execute(select(self.model).offset(skip).limit(limit))
            objs = list(result.scalars().all())

            duration = (time.time() - start) * 1000
            metrics_store.record_db_query(duration, True)
            return objs
        except Exception as e:
            metrics_store.record_db_query(0, False)
            raise e

    async def create(self, session: AsyncSession, *, obj_in: dict) -> ModelType:
        start = time.time()
        try:
            db_obj = self.model(**obj_in)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)

            duration = (time.time() - start) * 1000
            metrics_store.record_db_query(duration, True)
            return db_obj
        except Exception as e:
            await session.rollback()
            metrics_store.record_db_query(0, False)
            raise e
