from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ares.api.deps import get_db
from ares.db.tables import Base, User
from ares.main import app
from ares.services.auth_service import AuthService

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ares_test"

engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield async_session
        
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest_asyncio.fixture
async def test_user(async_session: AsyncSession) -> User:
    from ares.repositories.user_repo import UserRepository
    repo = UserRepository(async_session)
    user = repo.create_user(
        email="test@example.com", 
        hashed_password=AuthService.hash_password("password123"),
        display_name="Test User"
    )
    await async_session.commit()
    await async_session.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user: User) -> dict[str, str]:
    token = AuthService.create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}
