from fastapi import APIRouter, Depends

from app.core.dependencies import get_auth_service, get_current_user
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserPublic
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    return service.authenticate(payload.email, payload.password)


@router.get("/me", response_model=UserPublic)
def me(current_user=Depends(get_current_user)) -> UserPublic:
    return UserPublic(**current_user.model_dump(exclude={"hashed_password"}))
