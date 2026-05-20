from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_user_management_service
from app.schemas.pagination import PaginatedResponse
from app.schemas.user_management import UserCreate, UserPublic, UserRole, UserUpdate
from app.services.users_management import UserManagementService


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PaginatedResponse[UserPublic])
async def list_users(
    search: str | None = None,
    role: UserRole | None = Query(default=None),
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: UserManagementService = Depends(get_user_management_service),
    _user=Depends(get_current_user),
) -> dict:
    return await service.list(search=search, role=role, page=page, page_size=page_size)


@router.get("/me", response_model=UserPublic, summary="Mi perfil")
async def get_my_profile(
    user=Depends(get_current_user),
    service: UserManagementService = Depends(get_user_management_service),
) -> UserPublic:
    return await service.get(user.id)


@router.patch("/me", response_model=UserPublic, summary="Actualizar mi perfil")
async def update_my_profile(
    payload: UserUpdate,
    user=Depends(get_current_user),
    service: UserManagementService = Depends(get_user_management_service),
) -> UserPublic:
    return await service.update(user.id, payload)


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: int,
    service: UserManagementService = Depends(get_user_management_service),
    _user=Depends(get_current_user),
) -> UserPublic:
    return await service.get(user_id)


@router.post("", response_model=UserPublic)
async def create_user(
    payload: UserCreate,
    service: UserManagementService = Depends(get_user_management_service),
    _user=Depends(get_current_user),
) -> UserPublic:
    return await service.create(payload)


@router.patch("/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    service: UserManagementService = Depends(get_user_management_service),
    _user=Depends(get_current_user),
) -> UserPublic:
    return await service.update(user_id, payload)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserManagementService = Depends(get_user_management_service),
    _user=Depends(get_current_user),
) -> dict:
    await service.delete(user_id)
    return {"status": "ok"}
