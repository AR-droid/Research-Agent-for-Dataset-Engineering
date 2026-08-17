from __future__ import annotations

from fastapi import APIRouter
from ares.api.v1.auth import router as auth_router
from ares.api.v1.organizations import router as orgs_router
from ares.api.v1.projects import router as projects_router
from ares.api.v1.health import router as health_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(orgs_router, prefix="/organizations", tags=["organizations"])
api_router.include_router(projects_router, tags=["projects"])
api_router.include_router(health_router, tags=["health"])
