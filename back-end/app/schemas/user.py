from typing import Optional

from app.schemas.base import AppBaseModel


class UserPublic(AppBaseModel):
    id: int
    name: str
    last_name: Optional[str] = None
    ci: Optional[str] = None
    email: str
    role: str
    branch: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    active: bool = True
    client_number: Optional[int] = None


class UserInDB(UserPublic):
    hashed_password: str
