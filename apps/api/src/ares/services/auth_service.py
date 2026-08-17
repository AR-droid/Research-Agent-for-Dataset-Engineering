from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ares.config import get_settings
from ares.domain.exceptions import AuthenticationError, ConflictError
from ares.domain.models import TokenResponse, UserResponse
from ares.repositories.user_repo import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return str(pwd_context.hash(password))

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return bool(pwd_context.verify(plain, hashed))

    @staticmethod
    def create_access_token(user_id: UUID, role: str = "user") -> str:
        expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expire, "sub": str(user_id), "role": role, "type": "access"}
        return str(jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM))

    @staticmethod
    def create_refresh_token(user_id: UUID) -> str:
        expire = datetime.now(UTC) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode = {"exp": expire, "sub": str(user_id), "type": "refresh"}
        return str(jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM))

    @staticmethod
    def decode_token(token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            return payload # type: ignore
        except JWTError as e:
            raise AuthenticationError("Invalid or expired token") from e

    @staticmethod
    async def register(email: str, password: str, display_name: str | None, session: AsyncSession) -> UserResponse:
        repo = UserRepository(session)
        existing = await repo.get_by_email(email)
        if existing:
            raise ConflictError("Email already registered")
        
        user = repo.create_user(
            email=email,
            hashed_password=AuthService.hash_password(password),
            display_name=display_name
        )
        await session.commit()
        await session.refresh(user)
        return UserResponse.model_validate(user)

    @staticmethod
    async def login(email: str, password: str, session: AsyncSession) -> TokenResponse:
        repo = UserRepository(session)
        user = await repo.get_by_email(email)
        if not user or not AuthService.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid credentials")

        access = AuthService.create_access_token(user.id)
        refresh = AuthService.create_refresh_token(user.id)
        return TokenResponse(access_token=access, refresh_token=refresh)

    @staticmethod
    async def refresh(refresh_token: str, session: AsyncSession) -> TokenResponse:
        payload = AuthService.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise AuthenticationError("Invalid token type")
        
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise AuthenticationError("Invalid token payload")
        
        user_id = UUID(user_id_str)
        repo = UserRepository(session)
        user = await repo.get_by_id(user_id)
        if not user:
            raise AuthenticationError("User not found")
            
        access = AuthService.create_access_token(user.id)
        new_refresh = AuthService.create_refresh_token(user.id)
        return TokenResponse(access_token=access, refresh_token=new_refresh)
