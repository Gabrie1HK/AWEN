import io
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.dependencies import get_parcel_service, get_storage_service, require_permission
from app.database.database import get_db
from app.schemas.pagination import PaginatedResponse
from app.schemas.parcel import ParcelCreate, ParcelPublic, ParcelStatus, ParcelStatusUpdate, ParcelUpdate
from app.schemas.parcel_note import ParcelNoteCreate, ParcelNotePublic
from app.schemas.tracking import TrackingEvent
from app.services.parcels import ParcelService
from app.services.storage import StorageService
from app.schemas.user import UserInDB


router = APIRouter(prefix="/parcels", tags=["parcels"])


@router.get("", response_model=PaginatedResponse[ParcelPublic], summary="Listar encomiendas", dependencies=[Depends(require_permission())])
async def list_parcels(
    search: str | None = None,
    status: ParcelStatus | None = None,
    origin_branch: str | None = Query(default=None, alias="originBranch"),
    destination_branch: str | None = Query(default=None, alias="destinationBranch"),
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: ParcelService = Depends(get_parcel_service),
) -> dict:
    return await service.list(
        search=search,
        status=status,
        origin_branch=origin_branch,
        destination_branch=destination_branch,
        page=page,
        page_size=page_size,
    )


@router.get("/my-parcels", response_model=list[ParcelPublic], summary="Mis encomiendas (cliente)")
async def my_parcels(
    service: ParcelService = Depends(get_parcel_service),
    user: UserInDB = Depends(require_permission()),
) -> list[ParcelPublic]:
    return await service.list_by_user(user.name, user.last_name)


@router.get("/{parcel_id}", response_model=ParcelPublic, dependencies=[Depends(require_permission())])
async def get_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
) -> ParcelPublic:
    return await service.get(parcel_id)


@router.post("", response_model=ParcelPublic, summary="Crear encomienda", dependencies=[Depends(require_permission())])
async def create_parcel(
    payload: ParcelCreate,
    service: ParcelService = Depends(get_parcel_service),
) -> ParcelPublic:
    return await service.create(payload)


@router.patch("/{parcel_id}", response_model=ParcelPublic, dependencies=[Depends(require_permission())])
async def update_parcel(
    parcel_id: str,
    payload: ParcelUpdate,
    service: ParcelService = Depends(get_parcel_service),
) -> ParcelPublic:
    return await service.update(parcel_id, payload)


@router.post("/{parcel_id}/status", response_model=ParcelPublic)
async def update_status(
    parcel_id: str,
    payload: ParcelStatusUpdate,
    service: ParcelService = Depends(get_parcel_service),
    user: UserInDB = Depends(require_permission()),
) -> ParcelPublic:
    return await service.update_status(parcel_id, payload, driver_name=user.name)


@router.delete("/{parcel_id}", summary="Eliminar encomienda (admin)", dependencies=[Depends(require_permission())])
async def delete_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
) -> dict:
    await service.delete_parcel(parcel_id)
    return {"status": "ok"}


@router.post("/{parcel_id}/cancel", response_model=ParcelPublic, dependencies=[Depends(require_permission())])
async def cancel_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
) -> ParcelPublic:
    return await service.cancel(parcel_id)


@router.post("/{guide}/notes", response_model=ParcelNotePublic, status_code=201)
async def add_parcel_note(
    guide: str,
    payload: ParcelNoteCreate,
    service: ParcelService = Depends(get_parcel_service),
    db: AsyncSession = Depends(get_db),
    user: UserInDB = Depends(require_permission()),
) -> ParcelNotePublic:
    return await service.add_note(guide, payload.text, user.name, payload.is_public, db)


@router.get("/{guide}/notes", response_model=list[ParcelNotePublic], dependencies=[Depends(require_permission())])
async def get_parcel_notes(
    guide: str,
    service: ParcelService = Depends(get_parcel_service),
    db: AsyncSession = Depends(get_db),
) -> list[ParcelNotePublic]:
    return await service.get_notes(guide, db)


@router.post("/upload-evidence", summary="Subir foto de evidencia (retorna URL)", dependencies=[Depends(require_permission())])
async def upload_evidence(
    file: UploadFile = File(...),
    storage: StorageService = Depends(get_storage_service),
) -> dict:
    content = await file.read()
    file.filename = file.filename or "upload.bin"

    try:
        result = storage.upload_file(
            content=content,
            file_type="parcels",
            original_filename=file.filename,
            content_type=file.content_type or "application/octet-stream",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return result


@router.get("/{guide}/tracking", response_model=list[TrackingEvent], dependencies=[Depends(require_permission())])
async def parcel_tracking(
    guide: str,
    service: ParcelService = Depends(get_parcel_service),
) -> list[TrackingEvent]:
    events, _route = await service.tracking(guide)
    if not events:
        from app.core.errors import NotFoundError
        raise NotFoundError("Encomienda no encontrada")
    return events
