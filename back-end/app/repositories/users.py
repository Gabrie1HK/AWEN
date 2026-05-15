from __future__ import annotations

from typing import Dict, List, Optional

from app.schemas.user import UserInDB, UserPublic


class UserRepository:
    def get_by_email(self, email: str) -> Optional[UserInDB]:
        raise NotImplementedError

    def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        raise NotImplementedError

    def list(self) -> List[UserPublic]:
        raise NotImplementedError


class InMemoryUserRepository(UserRepository):
    def __init__(self, users: List[UserInDB]) -> None:
        self._users: Dict[int, UserInDB] = {u.id: u for u in users}
        self._by_email: Dict[str, int] = {u.email.lower(): u.id for u in users}

    def get_by_email(self, email: str) -> Optional[UserInDB]:
        user_id = self._by_email.get(email.lower())
        if user_id is None:
            return None
        return self._users.get(user_id)

    def get_by_id(self, user_id: int) -> Optional[UserInDB]:
        return self._users.get(user_id)

    def list(self) -> List[UserPublic]:
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
