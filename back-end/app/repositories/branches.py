from __future__ import annotations

from typing import Dict, List, Optional

from app.schemas.branch import BranchPublic, BranchUpdate


class BranchRepository:
    def list(self) -> List[BranchPublic]:
        raise NotImplementedError

    def get(self, branch_id: int) -> Optional[BranchPublic]:
        raise NotImplementedError

    def create(self, branch: BranchPublic) -> BranchPublic:
        raise NotImplementedError

    def update(self, branch_id: int, update: BranchUpdate) -> Optional[BranchPublic]:
        raise NotImplementedError

    def delete(self, branch_id: int) -> bool:
        raise NotImplementedError


class InMemoryBranchRepository(BranchRepository):
    def __init__(self, branches: List[BranchPublic]) -> None:
        self._branches: Dict[int, BranchPublic] = {b.id: b for b in branches}

    def list(self) -> List[BranchPublic]:
        return list(self._branches.values())

    def get(self, branch_id: int) -> Optional[BranchPublic]:
        return self._branches.get(branch_id)

    def create(self, branch: BranchPublic) -> BranchPublic:
        self._branches[branch.id] = branch
        return branch

    def update(self, branch_id: int, update: BranchUpdate) -> Optional[BranchPublic]:
        existing = self._branches.get(branch_id)
        if not existing:
            return None
        data = existing.model_dump()
        for key, value in update.model_dump(exclude_unset=True).items():
            data[key] = value
        updated = BranchPublic(**data)
        self._branches[branch_id] = updated
        return updated

    def delete(self, branch_id: int) -> bool:
        existing = self._branches.get(branch_id)
        if not existing:
            return False
        data = existing.model_dump()
        data["active"] = False
        self._branches[branch_id] = BranchPublic(**data)
        return True
