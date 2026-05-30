from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_parcel_service
from app.core.errors import NotFoundError
from app.database.database import get_db
from app.schemas.parcel import PublicTrackingParcel
from app.schemas.tracking import PublicTrackingResponse
from app.services.parcels import ParcelService


router = APIRouter(prefix="/tracking", tags=["tracking"])


@router.get("/{guide}", response_model=PublicTrackingResponse, summary="Tracking publico por guia")
async def public_tracking(
    guide: str,
    service: ParcelService = Depends(get_parcel_service),
    db: AsyncSession = Depends(get_db),
) -> PublicTrackingResponse:
    """Busca una encomienda por numero de guia y devuelve su estado, historial y notas publicas. No requiere autenticacion."""
    try:
        parcel = await service.get_by_guide(guide)
    except NotFoundError:
        return PublicTrackingResponse(guide=guide, parcel=None, history=None)

    public_parcel = PublicTrackingParcel(
        guide=parcel.guide,
        status=parcel.status,
        originBranch=parcel.origin_branch,
        destinationBranch=parcel.destination_branch,
        originAddress=parcel.origin_address,
        originLat=parcel.origin_lat,
        originLng=parcel.origin_lng,
        destinationAddress=parcel.destination_address,
        destinationLat=parcel.destination_lat,
        destinationLng=parcel.destination_lng,
        sender=parcel.sender,
        recipient=parcel.recipient,
        weight=parcel.weight,
    )
    history, route = await service.tracking(
        guide,
        origin=(parcel.origin_lat, parcel.origin_lng) if parcel.origin_lat is not None and parcel.origin_lng is not None else None,
        destination=(parcel.destination_lat, parcel.destination_lng) if parcel.destination_lat is not None and parcel.destination_lng is not None else None,
    )
    public_notes = await service.get_notes(guide, db, is_public_only=True)
    return PublicTrackingResponse(guide=guide, parcel=public_parcel, history=history, route=route, public_notes=public_notes)
