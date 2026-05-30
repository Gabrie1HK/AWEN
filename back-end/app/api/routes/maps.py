from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_parcel_service
from app.schemas.tracking import RouteResponse
from app.services.parcels import ParcelService


router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("/route", response_model=RouteResponse, summary="Calcular ruta entre dos puntos por calles")
async def get_route(
    origin_lat: float = Query(..., description="Latitud del origen"),
    origin_lng: float = Query(..., description="Longitud del origen"),
    destination_lat: float = Query(..., description="Latitud del destino"),
    destination_lng: float = Query(..., description="Longitud del destino"),
    service: ParcelService = Depends(get_parcel_service),
) -> RouteResponse:
    result = await service._build_route_from_points(
        (origin_lat, origin_lng),
        (destination_lat, destination_lng),
    )
    if not result:
        return RouteResponse(route=[], distance_km=0.0)
    return RouteResponse(**result)
