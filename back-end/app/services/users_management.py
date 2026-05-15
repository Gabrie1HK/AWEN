from __future__ import annotations

from app.core.errors import NotFoundError
from app.core.pagination import paginate
from app.repositories.user_management import UserManagementRepository
from app.schemas.user_management import UserCreate, UserPublic, UserRole, UserUpdate


class UserManagementService:
    def __init__(self, repo: UserManagementRepository) -> None:
        self._repo = repo

    def list(self, search: str | None = None, role: UserRole | None = None, page: int | None = None, page_size: int | None = None) -> list[UserPublic]:
        users = self._repo.list()
        if search:
            lowered = search.lower()
            users = [u for u in users if lowered in u.name.lower() or lowered in u.email.lower()]
        if role:
            users = [u for u in users if u.role == role]
        return paginate(users, page, page_size)

    def get(self, user_id: int) -> UserPublic:
        user = self._repo.get(user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        return user

    def create(self, payload: UserCreate) -> UserPublic:
        user_id = self._next_user_id()
        user = UserPublic(
            id=user_id,
            name=payload.name,
            email=payload.email,
            role=payload.role,
            branch=payload.branch,
            active=payload.active,
            lastLogin=payload.last_login,
        )
        return self._repo.create(user)

    def update(self, user_id: int, payload: UserUpdate) -> UserPublic:
        updated = self._repo.update(user_id, payload)
        if not updated:
            raise NotFoundError("Usuario no encontrado")
        return updated

    def delete(self, user_id: int) -> None:
        deleted = self._repo.delete(user_id)
        if not deleted:
            raise NotFoundError("Usuario no encontrado")

    def _next_user_id(self) -> int:
        existing = self._repo.list()
        if not existing:
            return 1
        return max(u.id for u in existing) + 1
