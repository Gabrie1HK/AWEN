from __future__ import annotations

from typing import Dict, List, Optional

from app.schemas.user_management import UserPublic, UserUpdate


class UserManagementRepository:
    def list(self) -> List[UserPublic]:
        raise NotImplementedError

    def get(self, user_id: int) -> Optional[UserPublic]:
        raise NotImplementedError

    def create(self, user: UserPublic) -> UserPublic:
        raise NotImplementedError

    def update(self, user_id: int, update: UserUpdate) -> Optional[UserPublic]:
        raise NotImplementedError

    def delete(self, user_id: int) -> bool:
        raise NotImplementedError


class InMemoryUserManagementRepository(UserManagementRepository):
    def __init__(self, users: List[UserPublic]) -> None:
        self._users: Dict[int, UserPublic] = {u.id: u for u in users}

    def list(self) -> List[UserPublic]:
        return list(self._users.values())

    def get(self, user_id: int) -> Optional[UserPublic]:
        return self._users.get(user_id)

    def create(self, user: UserPublic) -> UserPublic:
        self._users[user.id] = user
        return user

    def update(self, user_id: int, update: UserUpdate) -> Optional[UserPublic]:
        existing = self._users.get(user_id)
        if not existing:
            return None
        data = existing.model_dump(by_alias=True)
        for key, value in update.model_dump(by_alias=True, exclude_unset=True).items():
            data[key] = value
        updated = UserPublic(**data)
        self._users[user_id] = updated
        return updated

    def delete(self, user_id: int) -> bool:
        existing = self._users.get(user_id)
        if not existing:
            return False
        data = existing.model_dump(by_alias=True)
        data["active"] = False
        updated = UserPublic(**data)
        self._users[user_id] = updated
        return True
