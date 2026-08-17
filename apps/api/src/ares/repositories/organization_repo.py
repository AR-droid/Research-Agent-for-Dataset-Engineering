from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ares.db.tables import Membership, Organization
from ares.domain.enums import MembershipRole
from ares.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Organization)

    async def get_by_slug(self, slug: str) -> Organization | None:
        stmt = select(Organization).where(Organization.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_user_organizations(self, user_id: UUID) -> Sequence[Organization]:
        stmt = (
            select(Organization)
            .join(Membership, Organization.id == Membership.organization_id)
            .where(Membership.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def create_organization(self, name: str, slug: str) -> Organization:
        org = Organization(name=name, slug=slug)
        return self.create(org)

    def add_member(self, org_id: UUID, user_id: UUID, role: MembershipRole | str) -> Membership:
        membership = Membership(organization_id=org_id, user_id=user_id, role=str(role))
        self.session.add(membership)
        return membership

    async def get_membership(self, org_id: UUID, user_id: UUID) -> Membership | None:
        stmt = select(Membership).where(
            Membership.organization_id == org_id,
            Membership.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_members(self, org_id: UUID) -> Sequence[Membership]:
        stmt = select(Membership).where(Membership.organization_id == org_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
