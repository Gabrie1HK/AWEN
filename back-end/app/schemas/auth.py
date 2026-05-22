from pydantic import Field

from app.schemas.base import AppBaseModel
from app.schemas.user import UserPublic


class LoginRequest(AppBaseModel):
    email: str = Field(..., min_length=3, max_length=120)
    password: str = Field(..., min_length=1, max_length=120)


class TokenResponse(AppBaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
