from __future__ import annotations

from collections.abc import AsyncGenerator, Awaitable, Callable
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ares.db.engine import get_async_session
from ares.db.tables import Membership, User
from ares.domain.enums import MembershipRole, UserStatus
from ares.domain.exceptions import AuthenticationError
from ares.repositories.organization_repo import OrganizationRepository
from ares.repositories.user_repo import UserRepository
from ares.services.auth_service import AuthService

security = HTTPBearer()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_async_session():
        yield session

DbSession = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]

async def get_current_user(token: TokenDep, db: DbSession) -> User:
    try:
        payload = AuthService.decode_token(token.credentials)
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise AuthenticationError("Invalid token")
            
        user_id = UUID(user_id_str)
        repo = UserRepository(db)
        user = await repo.get_by_id(user_id)
        
        if not user:
            raise AuthenticationError("User not found")
        if user.status != UserStatus.ACTIVE:
            raise AuthenticationError("User inactive")
            
        return user
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

CurrentUser = Annotated[User, Depends(get_current_user)]

def require_role(*allowed_roles: MembershipRole) -> Callable[[UUID, CurrentUser, DbSession], Awaitable[Membership]]:
    async def role_checker(
        org_id: UUID, 
        user: CurrentUser, 
        db: DbSession
    ) -> Membership:
        repo = OrganizationRepository(db)
        membership = await repo.get_membership(org_id, user.id)
        
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Not a member of this organization"
            )
            
        if membership.role not in [role.value for role in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Insufficient permissions"
            )
            
        return membership
    return role_checker

async def get_org_membership(org_id: UUID, user: CurrentUser, db: DbSession) -> Membership:
    repo = OrganizationRepository(db)
    membership = await repo.get_membership(org_id, user.id)
    if not membership:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member")
    return membership
