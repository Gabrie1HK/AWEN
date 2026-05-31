import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings

from app.core.dependencies import get_current_user, get_parcel_service
from app.database.database import get_db
from app.schemas.pagination import PaginatedResponse
from app.schemas.parcel import ParcelCreate, ParcelPublic, ParcelStatus, ParcelStatusUpdate, ParcelUpdate
from app.schemas.parcel_note import ParcelNoteCreate, ParcelNotePublic
from app.schemas.tracking import TrackingEvent
from app.services.parcels import ParcelService


router = APIRouter(prefix="/parcels", tags=["parcels"])


@router.get("", response_model=PaginatedResponse[ParcelPublic], summary="Listar encomiendas")
async def list_parcels(
    search: str | None = None,
    status: ParcelStatus | None = None,
    origin_branch: str | None = Query(default=None, alias="originBranch"),
    destination_branch: str | None = Query(default=None, alias="destinationBranch"),
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
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
    user=Depends(get_current_user),
) -> list[ParcelPublic]:
    return await service.list_by_user(user.name, user.last_name)


@router.get("/{parcel_id}", response_model=ParcelPublic)
async def get_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return await service.get(parcel_id)


@router.post("", response_model=ParcelPublic, summary="Crear encomienda")
async def create_parcel(
    payload: ParcelCreate,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return await service.create(payload)


@router.patch("/{parcel_id}", response_model=ParcelPublic)
async def update_parcel(
    parcel_id: str,
    payload: ParcelUpdate,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return await service.update(parcel_id, payload)


@router.post("/{parcel_id}/status", response_model=ParcelPublic)
async def update_status(
    parcel_id: str,
    payload: ParcelStatusUpdate,
    service: ParcelService = Depends(get_parcel_service),
    user=Depends(get_current_user),
) -> ParcelPublic:
    return await service.update_status(parcel_id, payload, driver_name=user.name)


@router.delete("/{parcel_id}", summary="Eliminar encomienda (admin)")
async def delete_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> dict:
    await service.delete_parcel(parcel_id)
    return {"status": "ok"}


@router.post("/{parcel_id}/cancel", response_model=ParcelPublic)
async def cancel_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return await service.cancel(parcel_id)


@router.post("/{guide}/notes", response_model=ParcelNotePublic, status_code=201)
async def add_parcel_note(
    guide: str,
    payload: ParcelNoteCreate,
    service: ParcelService = Depends(get_parcel_service),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
) -> ParcelNotePublic:
    return await service.add_note(guide, payload.text, user.name, payload.is_public, db)


@router.get("/{guide}/notes", response_model=list[ParcelNotePublic])
async def get_parcel_notes(
    guide: str,
    service: ParcelService = Depends(get_parcel_service),
    db: AsyncSession = Depends(get_db),
    _user=Depends(get_current_user),
) -> list[ParcelNotePublic]:
    return await service.get_notes(guide, db)


@router.post("/upload-evidence", summary="Subir foto de evidencia (retorna URL)")
async def upload_evidence(
    file: UploadFile = File(...),
    _user=Depends(get_current_user),
) -> dict:
    settings = get_settings()
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix if file.filename else ".bin"
    filename = f"ev_{uuid.uuid4().hex}{ext}"
    filepath = upload_dir / filename

    content = await file.read()
    filepath.write_bytes(content)

    relative_url = f"/uploads/{filename}"
    return {"filename": filename, "url": relative_url, "size": len(content)}


@router.get("/{guide}/tracking", response_model=list[TrackingEvent])
async def parcel_tracking(
    guide: str,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> list[TrackingEvent]:
    events, _route = await service.tracking(guide)
    if not events:
        from app.core.errors import NotFoundError
        raise NotFoundError("Encomienda no encontrada")
    return events
