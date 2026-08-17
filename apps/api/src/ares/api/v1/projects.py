from __future__ import annotations

from uuid import UUID
from fastapi import APIRouter, Query
from ares.api.deps import DbSession, CurrentUser
from ares.domain.models import ProjectCreate, ProjectUpdate, ProjectResponse, PaginatedResponse
from ares.services.project_service import ProjectService

router = APIRouter()

@router.get("/organizations/{org_id}/projects", response_model=PaginatedResponse[ProjectResponse])
async def list_projects(
    org_id: UUID, 
    user: CurrentUser, 
    db: DbSession,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
) -> PaginatedResponse[ProjectResponse]:
    return await ProjectService.get_projects(org_id, user.id, db, offset, limit)

@router.post("/organizations/{org_id}/projects", response_model=ProjectResponse)
async def create_project(org_id: UUID, data: ProjectCreate, user: CurrentUser, db: DbSession) -> ProjectResponse:
    return await ProjectService.create_project(org_id, data, user.id, db)

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID, org_id: UUID, user: CurrentUser, db: DbSession) -> ProjectResponse:
    # org_id would typically come from query param or header for global endpoints
    return await ProjectService.get_project(project_id, org_id, user.id, db)

@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, org_id: UUID, data: ProjectUpdate, user: CurrentUser, db: DbSession) -> ProjectResponse:
    return await ProjectService.update_project(project_id, org_id, data, user.id, db)
