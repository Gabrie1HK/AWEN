from datetime import timedelta

from app.core.config import get_settings
from app.core.errors import UnauthorizedError
from app.core.security import create_access_token, decode_token, verify_password
from app.repositories.users import UserRepository
from app.schemas.auth import TokenResponse
from app.schemas.user import UserInDB, UserPublic


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def authenticate(self, email: str, password: str) -> TokenResponse:
        user = await self._repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Credenciales invalidas")
        if not user.active:
            raise UnauthorizedError("Error usuario inactivo, contacte al administrador")

        settings = get_settings()
        access_token = create_access_token(
            subject=str(user.id),
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
        )
        return TokenResponse(access_token=access_token, user=UserPublic(**user.model_dump(exclude={"hashed_password"})))

    async def get_current_user(self, token: str) -> UserInDB:
        try:
            payload = decode_token(token)
        except Exception as exc:  # noqa: BLE001
            raise UnauthorizedError("Token invalido") from exc

        subject = payload.get("sub")
        if not subject:
            raise UnauthorizedError("Token invalido")

        user = await self._repo.get_by_id(int(subject))
        if not user:
            raise UnauthorizedError("Usuario no encontrado")
        return user
