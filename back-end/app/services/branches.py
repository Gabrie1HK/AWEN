from __future__ import annotations

from typing import Any, Dict

from app.core.errors import NotFoundError
from app.core.pagination import paginate_with_meta
from app.repositories.branches import BranchRepository
from app.schemas.branch import BranchCreate, BranchPublic, BranchUpdate


class BranchService:
    def __init__(self, repo: BranchRepository) -> None:
        self._repo = repo

    async def list(self, search: str | None = None, page: int | None = None, page_size: int | None = None) -> Dict[str, Any]:
        branches = await self._repo.list()
        if search:
            lowered = search.lower()
            branches = [
                b for b in branches
                if lowered in b.name.lower() or lowered in b.city.lower()
            ]
        return paginate_with_meta(branches, page, page_size)

    async def get(self, branch_id: int) -> BranchPublic:
        branch = await self._repo.get(branch_id)
        if not branch:
            raise NotFoundError("Sucursal no encontrada")
        return branch

    async def create(self, payload: BranchCreate) -> BranchPublic:
        branch_id = await self._next_branch_id()
        branch = BranchPublic(id=branch_id, **payload.model_dump())
        return await self._repo.create(branch)

    async def update(self, branch_id: int, payload: BranchUpdate) -> BranchPublic:
        updated = await self._repo.update(branch_id, payload)
        if not updated:
            raise NotFoundError("Sucursal no encontrada")
        return updated

    async def delete(self, branch_id: int) -> None:
        deleted = await self._repo.delete(branch_id)
        if not deleted:
            raise NotFoundError("Sucursal no encontrada")

    async def _next_branch_id(self) -> int:
        existing = await self._repo.list()
        if not existing:
            return 1
        return max(b.id for b in existing) + 1
