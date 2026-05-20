from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_branch_service, get_current_user
from app.schemas.branch import BranchCreate, BranchPublic, BranchUpdate
from app.schemas.pagination import PaginatedResponse
from app.services.branches import BranchService


router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("", response_model=PaginatedResponse[BranchPublic])
async def list_branches(
    search: str | None = None,
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: BranchService = Depends(get_branch_service),
    _user=Depends(get_current_user),
) -> dict:
    return await service.list(search=search, page=page, page_size=page_size)


@router.get("/{branch_id}", response_model=BranchPublic)
async def get_branch(
    branch_id: int,
    service: BranchService = Depends(get_branch_service),
    _user=Depends(get_current_user),
) -> BranchPublic:
    return await service.get(branch_id)


@router.post("", response_model=BranchPublic)
async def create_branch(
    payload: BranchCreate,
    service: BranchService = Depends(get_branch_service),
    _user=Depends(get_current_user),
) -> BranchPublic:
    return await service.create(payload)


@router.patch("/{branch_id}", response_model=BranchPublic)
async def update_branch(
    branch_id: int,
    payload: BranchUpdate,
    service: BranchService = Depends(get_branch_service),
    _user=Depends(get_current_user),
) -> BranchPublic:
    return await service.update(branch_id, payload)


@router.delete("/{branch_id}")
async def delete_branch(
    branch_id: int,
    service: BranchService = Depends(get_branch_service),
    _user=Depends(get_current_user),
) -> dict:
    await service.delete(branch_id)
    return {"status": "ok"}
