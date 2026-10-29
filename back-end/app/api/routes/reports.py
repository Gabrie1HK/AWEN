from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse

from app.core.dependencies import get_report_service, require_permission
from app.schemas.reports import (
    ActivityItem,
    BranchDeliveryPoint,
    DailyShipmentPoint,
    KPIResponse,
    ReportSummary,
    RouteStat,
)
from app.services.reports import ReportService


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/kpis", response_model=KPIResponse, summary="KPIs principales", dependencies=[Depends(require_permission())])
async def report_kpis(
    date_from: str | None = Query(default=None, alias="dateFrom"),
    date_to: str | None = Query(default=None, alias="dateTo"),
    service: ReportService = Depends(get_report_service),
) -> KPIResponse:
    """Devuelve total de envios, en transito, entregados y devueltos."""
    return await service.kpis(date_from=date_from, date_to=date_to)


@router.get("/daily-volume", response_model=list[DailyShipmentPoint], dependencies=[Depends(require_permission())])
async def daily_volume(
    date_from: str | None = Query(default=None, alias="dateFrom"),
    date_to: str | None = Query(default=None, alias="dateTo"),
    service: ReportService = Depends(get_report_service),
) -> list[DailyShipmentPoint]:
    return await service.daily_shipments(date_from=date_from, date_to=date_to)


@router.get("/deliveries-by-branch", response_model=list[BranchDeliveryPoint], dependencies=[Depends(require_permission())])
async def deliveries_by_branch(
    service: ReportService = Depends(get_report_service),
) -> list[BranchDeliveryPoint]:
    return await service.deliveries_by_branch()


@router.get("/activity", response_model=list[ActivityItem], dependencies=[Depends(require_permission())])
async def recent_activity(
    service: ReportService = Depends(get_report_service),
) -> list[ActivityItem]:
    return await service.recent_activity()


@router.get("/summary", response_model=ReportSummary, dependencies=[Depends(require_permission())])
async def summary(
    service: ReportService = Depends(get_report_service),
) -> ReportSummary:
    return await service.summary()


@router.get("/top-routes", response_model=list[RouteStat], dependencies=[Depends(require_permission())])
async def top_routes(
    service: ReportService = Depends(get_report_service),
) -> list[RouteStat]:
    return await service.top_routes()


@router.get("/export", response_class=PlainTextResponse, summary="Exportar CSV", dependencies=[Depends(require_permission())])
async def export_csv(
    format: str = Query(default="csv"),
    service: ReportService = Depends(get_report_service),
) -> PlainTextResponse:
    if format != "csv":
        return PlainTextResponse("unsupported format", status_code=400)
    return PlainTextResponse(await service.export_csv(), media_type="text/csv")
