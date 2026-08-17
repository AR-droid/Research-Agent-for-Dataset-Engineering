from __future__ import annotations

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from ares.config import get_settings
from ares.api.v1 import api_router
from ares.db.engine import init_db, close_db
from ares.api.middleware import setup_middlewares

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield
    await close_db()

app = FastAPI(
    title='ARES API',
    version='0.1.0',
    lifespan=lifespan
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_middlewares(app)
app.include_router(api_router, prefix="/api/v1")
