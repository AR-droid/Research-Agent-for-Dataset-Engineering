from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ares.db.tables import ResearchProject
from ares.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[ResearchProject]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ResearchProject)

    async def get_by_org(self, org_id: UUID, offset: int = 0, limit: int = 100) -> Sequence[ResearchProject]:
        stmt = (
            select(ResearchProject)
            .where(ResearchProject.organization_id == org_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id_and_org(self, project_id: UUID, org_id: UUID) -> ResearchProject | None:
        stmt = select(ResearchProject).where(
            and_(
                ResearchProject.id == project_id,
                ResearchProject.organization_id == org_id
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    def create_project(self, project: ResearchProject) -> ResearchProject:
        return self.create(project)

    def update_project(self, project: ResearchProject) -> ResearchProject:
        return self.update(project)
