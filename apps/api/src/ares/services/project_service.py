from __future__ import annotations

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ares.domain.models import ProjectCreate, ProjectUpdate, ProjectResponse, PaginatedResponse
from ares.domain.exceptions import NotFoundError, AuthorizationError
from ares.domain.enums import MembershipRole
from ares.repositories.project_repo import ProjectRepository
from ares.repositories.organization_repo import OrganizationRepository
from ares.db.tables import ResearchProject

class ProjectService:
    @staticmethod
    async def create_project(org_id: UUID, data: ProjectCreate, user_id: UUID, session: AsyncSession) -> ProjectResponse:
        org_repo = OrganizationRepository(session)
        membership = await org_repo.get_membership(org_id, user_id)
        if not membership or membership.role in (MembershipRole.VIEWER, MembershipRole.REVIEWER):
            raise AuthorizationError("Insufficient permissions to create project")

        repo = ProjectRepository(session)
        project = ResearchProject(
            organization_id=org_id,
            name=data.name,
            description=data.description,
            research_question=data.research_question,
            inclusion_criteria=data.inclusion_criteria,
            exclusion_criteria=data.exclusion_criteria,
            date_from=data.date_from,
            date_to=data.date_to,
            created_by=user_id
        )
        repo.create_project(project)
        await session.commit()
        await session.refresh(project)
        return ProjectResponse.model_validate(project)

    @staticmethod
    async def get_projects(org_id: UUID, user_id: UUID, session: AsyncSession, offset: int = 0, limit: int = 100) -> PaginatedResponse[ProjectResponse]:
        org_repo = OrganizationRepository(session)
        membership = await org_repo.get_membership(org_id, user_id)
        if not membership:
            raise AuthorizationError("Not a member of this organization")

        repo = ProjectRepository(session)
        projects = await repo.get_by_org(org_id, offset, limit)
        
        items = [ProjectResponse.model_validate(p) for p in projects]
        return PaginatedResponse(
            items=items,
            total=len(items), # Simplified
            offset=offset,
            limit=limit,
            has_more=len(items) == limit
        )

    @staticmethod
    async def get_project(project_id: UUID, org_id: UUID, user_id: UUID, session: AsyncSession) -> ProjectResponse:
        org_repo = OrganizationRepository(session)
        membership = await org_repo.get_membership(org_id, user_id)
        if not membership:
            raise AuthorizationError("Not a member of this organization")

        repo = ProjectRepository(session)
        project = await repo.get_by_id_and_org(project_id, org_id)
        if not project:
            raise NotFoundError("Project not found")

        return ProjectResponse.model_validate(project)

    @staticmethod
    async def update_project(project_id: UUID, org_id: UUID, data: ProjectUpdate, user_id: UUID, session: AsyncSession) -> ProjectResponse:
        org_repo = OrganizationRepository(session)
        membership = await org_repo.get_membership(org_id, user_id)
        if not membership or membership.role == MembershipRole.VIEWER:
            raise AuthorizationError("Insufficient permissions to update project")

        repo = ProjectRepository(session)
        project = await repo.get_by_id_and_org(project_id, org_id)
        if not project:
            raise NotFoundError("Project not found")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project, key, value)

        await session.commit()
        await session.refresh(project)
        return ProjectResponse.model_validate(project)
