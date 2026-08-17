from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ares.db.tables import Base


class BaseRepository[T: Base]:
    def __init__(self, session: AsyncSession, model_cls: type[T]) -> None:
        self.session = session
        self.model_cls = model_cls

    async def get_by_id(self, id: UUID) -> T | None:
        return await self.session.get(self.model_cls, id)

    async def get_all(self, offset: int = 0, limit: int = 100) -> Sequence[T]:
        stmt = select(self.model_cls).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def create(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def update(self, entity: T) -> T:
        return entity  # With ORM, changes are tracked automatically

    async def delete(self, id: UUID) -> None:
        entity = await self.get_by_id(id)
        if entity:
            await self.session.delete(entity)
