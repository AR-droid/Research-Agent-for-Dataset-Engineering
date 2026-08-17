from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import text

from ares.api.deps import DbSession
from ares.domain.models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")

@router.get("/ready", response_model=HealthResponse)
async def readiness_check(db: DbSession) -> HealthResponse:
    db_status = "ok"
    from sqlalchemy.exc import SQLAlchemyError
    try:
        await db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "error"
        
    return HealthResponse(
        status="ok" if db_status == "ok" else "error",
        database=db_status,
        redis="ok" # Placeholder for redis check
    )
