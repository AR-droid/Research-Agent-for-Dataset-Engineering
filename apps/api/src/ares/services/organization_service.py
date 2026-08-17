from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ares.domain.enums import MembershipRole
from ares.domain.exceptions import AuthorizationError, ConflictError, NotFoundError
from ares.domain.models import MembershipResponse, OrganizationResponse
from ares.repositories.organization_repo import OrganizationRepository


class OrganizationService:
    @staticmethod
    async def create_organization(name: str, slug: str, user_id: UUID, session: AsyncSession) -> OrganizationResponse:
        repo = OrganizationRepository(session)
        existing = await repo.get_by_slug(slug)
        if existing:
            raise ConflictError("Organization slug already in use")

        org = repo.create_organization(name=name, slug=slug)
        await session.flush()
        repo.add_member(org.id, user_id, MembershipRole.OWNER)
        await session.commit()
        await session.refresh(org)
        return OrganizationResponse.model_validate(org)

    @staticmethod
    async def get_user_organizations(user_id: UUID, session: AsyncSession) -> list[OrganizationResponse]:
        repo = OrganizationRepository(session)
        orgs = await repo.get_user_organizations(user_id)
        return [OrganizationResponse.model_validate(org) for org in orgs]

    @staticmethod
    async def get_organization(org_id: UUID, user_id: UUID, session: AsyncSession) -> OrganizationResponse:
        repo = OrganizationRepository(session)
        membership = await repo.get_membership(org_id, user_id)
        if not membership:
            raise AuthorizationError("Not a member of this organization")

        org = await repo.get_by_id(org_id)
        if not org:
            raise NotFoundError("Organization not found")
        return OrganizationResponse.model_validate(org)

    @staticmethod
    async def add_member(org_id: UUID, user_id: UUID, role: MembershipRole, current_user_id: UUID, session: AsyncSession) -> MembershipResponse:
        repo = OrganizationRepository(session)
        current_membership = await repo.get_membership(org_id, current_user_id)
        if not current_membership or current_membership.role not in (MembershipRole.OWNER, MembershipRole.ADMIN):
            raise AuthorizationError("Insufficient permissions to add members")

        existing_membership = await repo.get_membership(org_id, user_id)
        if existing_membership:
            raise ConflictError("User is already a member")

        membership = repo.add_member(org_id, user_id, role)
        await session.commit()
        await session.refresh(membership)
        return MembershipResponse.model_validate(membership)
