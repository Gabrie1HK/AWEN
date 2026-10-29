from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_user_management_service, require_permission
from app.schemas.pagination import PaginatedResponse
from app.schemas.user_management import UserCreate, UserPasswordReset, UserPublic, UserRole, UserUpdate
from app.services.users_management import UserManagementService
from app.schemas.user import UserInDB


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PaginatedResponse[UserPublic], dependencies=[Depends(require_permission())])
async def list_users(
    search: str | None = None,
    role: UserRole | None = Query(default=None),
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: UserManagementService = Depends(get_user_management_service),
) -> dict:
    return await service.list(search=search, role=role, page=page, page_size=page_size)


@router.get("/me", response_model=UserPublic, summary="Mi perfil")
async def get_my_profile(
    user: UserInDB = Depends(require_permission()),
    service: UserManagementService = Depends(get_user_management_service),
) -> UserPublic:
    return await service.get(user.id)


@router.patch("/me", response_model=UserPublic, summary="Actualizar mi perfil")
async def update_my_profile(
    payload: UserUpdate,
    user: UserInDB = Depends(require_permission()),
    service: UserManagementService = Depends(get_user_management_service),
) -> UserPublic:
    return await service.update(user.id, payload)


@router.get("/{user_id}", response_model=UserPublic, dependencies=[Depends(require_permission())])
async def get_user(
    user_id: int,
    service: UserManagementService = Depends(get_user_management_service),
) -> UserPublic:
    return await service.get(user_id)


@router.post("", response_model=UserPublic, dependencies=[Depends(require_permission())])
async def create_user(
    payload: UserCreate,
    service: UserManagementService = Depends(get_user_management_service),
) -> UserPublic:
    return await service.create(payload)


@router.patch("/{user_id}", response_model=UserPublic, dependencies=[Depends(require_permission())])
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserManagementService = Depends(get_user_management_service),
) -> UserPublic:
    return await service.update(user_id, payload)


@router.delete("/{user_id}", dependencies=[Depends(require_permission())])
async def delete_user(
    user_id: int,
    service: UserManagementService = Depends(get_user_management_service),
) -> dict:
    await service.delete(user_id)
    return {"status": "ok"}


@router.patch("/{user_id}/password", summary="Cambiar clave de usuario (admin)", dependencies=[Depends(require_permission())])
async def reset_user_password(
    user_id: int,
    payload: UserPasswordReset,
    service: UserManagementService = Depends(get_user_management_service),
) -> dict:
    await service.reset_password(user_id, payload.new_password)
    return {"status": "ok"}
