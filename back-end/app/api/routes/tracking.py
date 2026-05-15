from fastapi import APIRouter, Depends

from app.core.dependencies import get_parcel_service
from app.schemas.parcel import PublicTrackingParcel
from app.schemas.tracking import PublicTrackingResponse
from app.services.parcels import ParcelService


router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.get("/{guide}", response_model=PublicTrackingResponse)
def public_tracking(
    guide: str,
    service: ParcelService = Depends(get_parcel_service),
) -> PublicTrackingResponse:
    try:
        parcel = service.get_by_guide(guide)
    except Exception:
        return PublicTrackingResponse(guide=guide, parcel=None, history=None)

    public_parcel = PublicTrackingParcel(
        guide=parcel.guide,
        status=parcel.status,
        originBranch=parcel.origin_branch,
        destinationBranch=parcel.destination_branch,
        sender=parcel.sender,
        recipient=parcel.recipient,
        weight=parcel.weight,
    )
    history = service.tracking(guide)
    return PublicTrackingResponse(guide=guide, parcel=public_parcel, history=history)
