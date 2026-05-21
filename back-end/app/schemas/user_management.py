from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import Field

from app.schemas.base import AppBaseModel


class UserRole(str, Enum):
    ADMIN = "Admin"
    WAREHOUSE = "Warehouse Operator"
    DRIVER = "Driver"
    CLIENT = "Client"


class UserBase(AppBaseModel):
    name: str
    email: str
    role: UserRole
    branch: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    active: bool = True
    last_login: Optional[str] = Field(default=None, alias="lastLogin")


class UserCreate(UserBase):
    pass


class UserUpdate(AppBaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None
    branch: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    active: Optional[bool] = None
    last_login: Optional[str] = Field(default=None, alias="lastLogin")

class UserPublic(UserBase):
    id: int
