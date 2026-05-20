from __future__ import annotations

from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.branch import Branch
from app.schemas.branch import BranchPublic, BranchUpdate


class BranchRepository:
    async def list(self) -> List[BranchPublic]:
        raise NotImplementedError

    async def get(self, branch_id: int) -> Optional[BranchPublic]:
        raise NotImplementedError

    async def create(self, branch: BranchPublic) -> BranchPublic:
        raise NotImplementedError

    async def update(self, branch_id: int, update: BranchUpdate) -> Optional[BranchPublic]:
        raise NotImplementedError

    async def delete(self, branch_id: int) -> bool:
        raise NotImplementedError


class InMemoryBranchRepository(BranchRepository):
    def __init__(self, branches: List[BranchPublic]) -> None:
        self._branches: Dict[int, BranchPublic] = {b.id: b for b in branches}

    async def list(self) -> List[BranchPublic]:
        return list(self._branches.values())

    async def get(self, branch_id: int) -> Optional[BranchPublic]:
        return self._branches.get(branch_id)

    async def create(self, branch: BranchPublic) -> BranchPublic:
        self._branches[branch.id] = branch
        return branch

    async def update(self, branch_id: int, update: BranchUpdate) -> Optional[BranchPublic]:
        existing = self._branches.get(branch_id)
        if not existing:
            return None
        data = existing.model_dump()
        for key, value in update.model_dump(exclude_unset=True).items():
            data[key] = value
        updated = BranchPublic(**data)
        self._branches[branch_id] = updated
        return updated

    async def delete(self, branch_id: int) -> bool:
        existing = self._branches.get(branch_id)
        if not existing:
            return False
        data = existing.model_dump()
        data["active"] = False
        self._branches[branch_id] = BranchPublic(**data)
        return True


class SqlAlchemyBranchRepository(BranchRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self) -> List[BranchPublic]:
        result = await self._session.execute(select(Branch))
        items = result.scalars().all()
        return [
            BranchPublic(
                id=b.id,
                name=b.name,
                city=b.city,
                address=b.address,
                manager=b.manager,
                phone=b.phone,
                active=b.active,
            )
            for b in items
        ]

    async def get(self, branch_id: int) -> Optional[BranchPublic]:
        branch = await self._session.get(Branch, branch_id)
        if not branch:
            return None
        return BranchPublic(
            id=branch.id,
            name=branch.name,
            city=branch.city,
            address=branch.address,
            manager=branch.manager,
            phone=branch.phone,
            active=branch.active,
        )

    async def create(self, branch: BranchPublic) -> BranchPublic:
        record = Branch(
            id=branch.id,
            name=branch.name,
            city=branch.city,
            address=branch.address,
            manager=branch.manager,
            phone=branch.phone,
            active=branch.active,
        )
        self._session.add(record)
        await self._session.commit()
        return branch

    async def update(self, branch_id: int, update: BranchUpdate) -> Optional[BranchPublic]:
        branch = await self._session.get(Branch, branch_id)
        if not branch:
            return None
        for key, value in update.model_dump(exclude_unset=True).items():
            setattr(branch, key, value)
        await self._session.commit()
        return BranchPublic(
            id=branch.id,
            name=branch.name,
            city=branch.city,
            address=branch.address,
            manager=branch.manager,
            phone=branch.phone,
            active=branch.active,
        )

    async def delete(self, branch_id: int) -> bool:
        branch = await self._session.get(Branch, branch_id)
        if not branch:
            return False
        branch.active = False
        await self._session.commit()
        return True
