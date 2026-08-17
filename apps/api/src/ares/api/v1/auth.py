from __future__ import annotations

from fastapi import APIRouter, status
from pydantic import BaseModel

from ares.api.deps import CurrentUser, DbSession
from ares.domain.models import TokenResponse, UserCreate, UserLogin, UserResponse
from ares.services.auth_service import AuthService

router = APIRouter()

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: DbSession) -> UserResponse:
    return await AuthService.register(data.email, data.password, data.display_name, db)

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: DbSession) -> TokenResponse:
    return await AuthService.login(data.email, data.password, db)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: DbSession) -> TokenResponse:
    return await AuthService.refresh(data.refresh_token, db)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(current_user: CurrentUser) -> None:
    # Client drops the token, server might blacklist it in a full implementation
    pass

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)
