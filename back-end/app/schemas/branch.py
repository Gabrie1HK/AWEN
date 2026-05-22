from __future__ import annotations

from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel


class BranchBase(AppBaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    city: str = Field(..., min_length=1, max_length=120)
    address: str = Field(..., min_length=1, max_length=200)
    manager: str = Field(..., min_length=1, max_length=120)
    phone: str = Field(..., min_length=1, max_length=40)
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
