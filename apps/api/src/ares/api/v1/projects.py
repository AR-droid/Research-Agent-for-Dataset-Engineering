from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query

from ares.api.deps import CurrentUser, DbSession
from ares.domain.models import PaginatedResponse, ProjectCreate, ProjectResponse, ProjectUpdate
from pydantic import BaseModel
from ares.worker.tasks import execute_workflow
from ares.domain.enums import AgentRunStatus
from ares.services.project_service import ProjectService

class AgentRunCreate(BaseModel):
    run_type: str

class AgentRunResponse(BaseModel):
    id: UUID
    project_id: UUID
    run_type: str
    status: str

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

from sqlalchemy import select
from ares.db.tables import AgentRun
import redis.asyncio as aioredis
from ares.config import get_settings
import json

@router.post("/projects/{project_id}/runs", response_model=AgentRunResponse)
async def start_agent_run(project_id: UUID, data: AgentRunCreate, user: CurrentUser, db: DbSession) -> AgentRunResponse:
    # Create the run in the database
    new_run = AgentRun(
        project_id=project_id,
        run_type=data.run_type,
        status=AgentRunStatus.QUEUED,
        current_stage="PLANNING"
    )
    db.add(new_run)
    await db.commit()
    await db.refresh(new_run)
    
    # Trigger celery task
    execute_workflow.delay(str(new_run.id))
    
    return AgentRunResponse(
        id=new_run.id,
        project_id=new_run.project_id,
        run_type=new_run.run_type,
        status=new_run.status
    )

async def _publish_api_event(run_id: UUID, status: str, message: str = "") -> None:
    settings = get_settings()
    redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)  # type: ignore
    msg = json.dumps({"run_id": str(run_id), "status": status, "message": message})
    await redis_client.publish(f"agent_run_{run_id}", msg)
    await redis_client.aclose()

@router.post("/runs/{run_id}/cancel")
async def cancel_run(run_id: UUID, user: CurrentUser, db: DbSession) -> dict[str, str | UUID]:
    stmt = select(AgentRun).where(AgentRun.id == run_id)
    result = await db.execute(stmt)
    agent_run = result.scalar_one_or_none()
    if agent_run:
        agent_run.status = AgentRunStatus.CANCELLED
        await db.commit()
        await _publish_api_event(run_id, AgentRunStatus.CANCELLED, "Run cancelled by user")
    return {"status": "cancelled", "run_id": run_id}

@router.post("/runs/{run_id}/resume")
async def resume_run(run_id: UUID, user: CurrentUser, db: DbSession) -> dict[str, str | UUID]:
    stmt = select(AgentRun).where(AgentRun.id == run_id)
    result = await db.execute(stmt)
    agent_run = result.scalar_one_or_none()
    if agent_run:
        if agent_run.status == AgentRunStatus.PAUSED:
            agent_run.status = AgentRunStatus.RUNNING
            await db.commit()
            await _publish_api_event(run_id, AgentRunStatus.RUNNING, "Run resumed by user")
            # If the task was completely stopped, we might need to kick it off again:
            execute_workflow.delay(str(agent_run.id))
    return {"status": "resumed", "run_id": run_id}

@router.post("/runs/{run_id}/approve")
async def approve_run(run_id: UUID, user: CurrentUser, db: DbSession) -> dict[str, str | UUID]:
    stmt = select(AgentRun).where(AgentRun.id == run_id)
    result = await db.execute(stmt)
    agent_run = result.scalar_one_or_none()
    if agent_run:
        if agent_run.status == AgentRunStatus.REQUIRES_REVIEW:
            agent_run.status = AgentRunStatus.RUNNING
            await db.commit()
            await _publish_api_event(run_id, AgentRunStatus.RUNNING, "Run approved by user")
            # Kick off worker again to continue from the next stage
            execute_workflow.delay(str(agent_run.id))
    return {"status": "approved", "run_id": run_id}
