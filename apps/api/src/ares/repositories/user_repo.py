from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ares.db.tables import User
from ares.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    def create_user(self, email: str, hashed_password: str, display_name: str | None = None) -> User:
        user = User(email=email, hashed_password=hashed_password, display_name=display_name)
        return self.create(user)
