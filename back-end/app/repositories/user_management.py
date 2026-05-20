from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_management import UserManagement
from app.schemas.user_management import UserPublic, UserUpdate


class UserManagementRepository:
    async def list(self) -> List[UserPublic]:
        raise NotImplementedError

    async def get(self, user_id: int) -> Optional[UserPublic]:
        raise NotImplementedError

    async def create(self, user: UserPublic) -> UserPublic:
        raise NotImplementedError

    async def update(self, user_id: int, update: UserUpdate) -> Optional[UserPublic]:
        raise NotImplementedError

    async def delete(self, user_id: int) -> bool:
        raise NotImplementedError


class InMemoryUserManagementRepository(UserManagementRepository):
    def __init__(self, users: List[UserPublic]) -> None:
        self._users: Dict[int, UserPublic] = {u.id: u for u in users}

    async def list(self) -> List[UserPublic]:
        return list(self._users.values())

    async def get(self, user_id: int) -> Optional[UserPublic]:
        return self._users.get(user_id)

    async def create(self, user: UserPublic) -> UserPublic:
        self._users[user.id] = user
        return user

    async def update(self, user_id: int, update: UserUpdate) -> Optional[UserPublic]:
        existing = self._users.get(user_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        for key, value in update.model_dump(by_alias=True, exclude_unset=True).items():
            data[key] = value
        updated = UserPublic(**data)
        self._users[user_id] = updated
        return updated

    async def delete(self, user_id: int) -> bool:
        existing = self._users.get(user_id)
        if not existing:
            return False
        data = existing.model_dump(by_alias=True)
        data["active"] = False
        updated = UserPublic(**data)
        self._users[user_id] = updated
        return True


class SqlAlchemyUserManagementRepository(UserManagementRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[UserPublic]:
        result = await self._session.execute(select(UserManagement))
        users = result.scalars().all()
        return [
            UserPublic(
                id=u.id,
                name=u.name,
                email=u.email,
                role=u.role,
                branch=u.branch,
                phone=u.phone,
                address=u.address,
                active=u.active,
                lastLogin=u.last_login,
            )
            for u in users
        ]

    async def get(self, user_id: int) -> Optional[UserPublic]:
        user = await self._session.get(UserManagement, user_id)
        if not user:
            return None
        return UserPublic(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            branch=user.branch,
            phone=user.phone,
            address=user.address,
            active=user.active,
            lastLogin=user.last_login,
        )

    async def create(self, user: UserPublic) -> UserPublic:
        record = UserManagement(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            branch=user.branch,
            phone=user.phone,
            address=user.address,
            active=user.active,
            last_login=user.last_login,
        )
        self._session.add(record)
        await self._session.commit()
        return user

    async def update(self, user_id: int, update: UserUpdate) -> Optional[UserPublic]:
        user = await self._session.get(UserManagement, user_id)
        if not user:
            return None
        data = update.model_dump(by_alias=True, exclude_unset=True)
        if "lastLogin" in data:
            user.last_login = data.pop("lastLogin")
        for key, value in data.items():
            setattr(user, key, value)
        await self._session.commit()
        return UserPublic(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            branch=user.branch,
            phone=user.phone,
            address=user.address,
            active=user.active,
            lastLogin=user.last_login,
        )

    async def delete(self, user_id: int) -> bool:
        user = await self._session.get(UserManagement, user_id)
        if not user:
            return False
        user.active = False
        await self._session.commit()
        return True
