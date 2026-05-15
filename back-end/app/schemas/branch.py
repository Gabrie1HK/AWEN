from __future__ import annotations

from typing import Optional

from app.schemas.base import AppBaseModel


class BranchBase(AppBaseModel):
    name: str
    city: str
    address: str
    manager: str
    phone: str
    active: bool = True


class BranchCreate(BranchBase):
    pass


class BranchUpdate(AppBaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    manager: Optional[str] = None
    phone: Optional[str] = None
    active: Optional[bool] = None


class BranchPublic(BranchBase):
    id: int
