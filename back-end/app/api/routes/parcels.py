from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_current_user, get_parcel_service
from app.schemas.parcel import ParcelCreate, ParcelPublic, ParcelStatus, ParcelStatusUpdate, ParcelUpdate
from app.schemas.tracking import TrackingEvent
from app.services.parcels import ParcelService


router = APIRouter(prefix="/parcels", tags=["parcels"])


@router.get("", response_model=list[ParcelPublic])
def list_parcels(
    search: str | None = None,
    status: ParcelStatus | None = None,
    origin_branch: str | None = Query(default=None, alias="originBranch"),
    destination_branch: str | None = Query(default=None, alias="destinationBranch"),
    page: int | None = Query(default=None, ge=1),
    page_size: int | None = Query(default=None, ge=1, le=200, alias="pageSize"),
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> list[ParcelPublic]:
    return service.list(
        search=search,
        status=status,
        origin_branch=origin_branch,
        destination_branch=destination_branch,
        page=page,
        page_size=page_size,
    )


@router.get("/{parcel_id}", response_model=ParcelPublic)
def get_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return service.get(parcel_id)


@router.post("", response_model=ParcelPublic)
def create_parcel(
    payload: ParcelCreate,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return service.create(payload)


@router.patch("/{parcel_id}", response_model=ParcelPublic)
def update_parcel(
    parcel_id: str,
    payload: ParcelUpdate,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return service.update(parcel_id, payload)


@router.post("/{parcel_id}/status", response_model=ParcelPublic)
def update_status(
    parcel_id: str,
    payload: ParcelStatusUpdate,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return service.update_status(parcel_id, payload)


@router.post("/{parcel_id}/cancel", response_model=ParcelPublic)
def cancel_parcel(
    parcel_id: str,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> ParcelPublic:
    return service.cancel(parcel_id)


@router.get("/{guide}/tracking", response_model=list[TrackingEvent])
def parcel_tracking(
    guide: str,
    service: ParcelService = Depends(get_parcel_service),
    _user=Depends(get_current_user),
) -> list[TrackingEvent]:
    service.get_by_guide(guide)
    return service.tracking(guide)
