from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserInDB, UserPublic


class UserRepository:
    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        raise NotImplementedError

    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        raise NotImplementedError

    async def list(self) -> List[UserPublic]:
        raise NotImplementedError


class InMemoryUserRepository(UserRepository):
    def __init__(self, users: List[UserInDB]) -> None:
        self._users: Dict[int, UserInDB] = {u.id: u for u in users}
        self._by_email: Dict[str, int] = {u.email.lower(): u.id for u in users}

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        user_id = self._by_email.get(email.lower())
        if user_id is None:
            return None
        return self._users.get(user_id)

    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        return self._users.get(user_id)

    async def list(self) -> List[UserPublic]:
        return [
            UserPublic(
                id=u.id,
                name=u.name,
                email=u.email,
                role=u.role,
                branch=u.branch,
                active=u.active,
            )
            for u in self._users.values()
        ]


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> Optional[UserInDB]:
        result = await self._session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserInDB(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            branch=user.branch,
            phone=user.phone,
            address=user.address,
            active=user.active,
            hashed_password=user.hashed_password,
        )

    async def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        user = await self._session.get(User, user_id)
        if not user:
            return None
        return UserInDB(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            branch=user.branch,
            phone=user.phone,
            address=user.address,
            active=user.active,
            hashed_password=user.hashed_password,
        )

    async def list(self) -> List[UserPublic]:
        result = await self._session.execute(select(User))
        users = result.scalars().all()
        return [
            UserPublic(
                id=u.id,
                name=u.name,
                email=u.email,
                role=u.role,
                branch=u.branch,
                active=u.active,
            )
            for u in users
        ]
