from app.schemas.base import AppBaseModel
from app.schemas.user import UserPublic


class LoginRequest(AppBaseModel):
    email: str
    password: str


class TokenResponse(AppBaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
