from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends

from ares.api.deps import CurrentUser, DbSession, require_role
from ares.domain.enums import MembershipRole
from ares.domain.models import (
    MembershipCreate,
    MembershipResponse,
    OrganizationCreate,
    OrganizationResponse,
)
from ares.services.organization_service import OrganizationService

router = APIRouter()

@router.get("", response_model=list[OrganizationResponse])
async def list_organizations(user: CurrentUser, db: DbSession) -> list[OrganizationResponse]:
    return await OrganizationService.get_user_organizations(user.id, db)

@router.post("", response_model=OrganizationResponse)
async def create_organization(data: OrganizationCreate, user: CurrentUser, db: DbSession) -> OrganizationResponse:
    return await OrganizationService.create_organization(data.name, data.slug, user.id, db)

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(org_id: UUID, user: CurrentUser, db: DbSession) -> OrganizationResponse:
    return await OrganizationService.get_organization(org_id, user.id, db)

@router.get("/{org_id}/members", response_model=list[MembershipResponse])
async def list_members(org_id: UUID, user: CurrentUser, db: DbSession) -> list[MembershipResponse]:
    # Placeholder: assuming get_organization checks if user is a member
    await OrganizationService.get_organization(org_id, user.id, db)
    from ares.repositories.organization_repo import OrganizationRepository
    repo = OrganizationRepository(db)
    members = await repo.get_members(org_id)
    return [MembershipResponse.model_validate(m) for m in members]

@router.post("/{org_id}/members", response_model=MembershipResponse)
async def add_member(
    org_id: UUID, 
    data: MembershipCreate, 
    user: CurrentUser, 
    db: DbSession,
    _: Any = Depends(require_role(MembershipRole.OWNER, MembershipRole.ADMIN)) # noqa: B008
) -> MembershipResponse:
    return await OrganizationService.add_member(org_id, data.user_id, data.role, user.id, db)
