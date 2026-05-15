from __future__ import annotations

from app.core.errors import NotFoundError
from app.core.pagination import paginate
from app.repositories.branches import BranchRepository
from app.schemas.branch import BranchCreate, BranchPublic, BranchUpdate


class BranchService:
    def __init__(self, repo: BranchRepository) -> None:
        self._repo = repo

    def list(self, search: str | None = None, page: int | None = None, page_size: int | None = None) -> list[BranchPublic]:
        branches = self._repo.list()
        if search:
            lowered = search.lower()
            branches = [
                b for b in branches
                if lowered in b.name.lower() or lowered in b.city.lower()
            ]
        return paginate(branches, page, page_size)

    def get(self, branch_id: int) -> BranchPublic:
        branch = self._repo.get(branch_id)
        if not branch:
            raise NotFoundError("Sucursal no encontrada")
        return branch

    def create(self, payload: BranchCreate) -> BranchPublic:
        branch_id = self._next_branch_id()
        branch = BranchPublic(id=branch_id, **payload.model_dump())
        return self._repo.create(branch)

    def update(self, branch_id: int, payload: BranchUpdate) -> BranchPublic:
        updated = self._repo.update(branch_id, payload)
        if not updated:
            raise NotFoundError("Sucursal no encontrada")
        return updated

    def delete(self, branch_id: int) -> None:
        deleted = self._repo.delete(branch_id)
        if not deleted:
            raise NotFoundError("Sucursal no encontrada")

    def _next_branch_id(self) -> int:
        existing = self._repo.list()
        if not existing:
            return 1
        return max(b.id for b in existing) + 1
