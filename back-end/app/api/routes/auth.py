from fastapi import APIRouter, Depends

from app.core.dependencies import get_auth_service, require_permission
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserPublic, UserInDB
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesion")
async def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    """Autentica al usuario con email y password, devuelve un JWT."""
    return await service.authenticate(payload.email, payload.password)


@router.get("/me", response_model=UserPublic, summary="Obtener usuario actual", dependencies=[Depends(require_permission("GET", "/api/v1/auth/me"))])
async def me(current_user: UserInDB = Depends(require_permission("GET", "/api/v1/auth/me"))) -> UserPublic:
    """Devuelve la informacion del usuario autenticado segun el token JWT."""
    return UserPublic(**current_user.model_dump(exclude={"hashed_password"}))
