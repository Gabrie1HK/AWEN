from typing import Optional

from app.schemas.base import AppBaseModel


class UserPublic(AppBaseModel):
    id: int
    name: str
    email: str
    role: str
    branch: Optional[str] = None
    active: bool = True


class UserInDB(UserPublic):
    hashed_password: str
