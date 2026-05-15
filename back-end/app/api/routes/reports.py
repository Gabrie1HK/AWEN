from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse

from app.core.dependencies import get_current_user, get_report_service
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


@router.get("/kpis", response_model=KPIResponse, summary="KPIs principales")
def report_kpis(
    date_from: str | None = Query(default=None, alias="dateFrom"),
    date_to: str | None = Query(default=None, alias="dateTo"),
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> KPIResponse:
    """Devuelve total de envios, en transito, entregados y devueltos."""
    return service.kpis(date_from=date_from, date_to=date_to)


@router.get("/daily-volume", response_model=list[DailyShipmentPoint])
def daily_volume(
    date_from: str | None = Query(default=None, alias="dateFrom"),
    date_to: str | None = Query(default=None, alias="dateTo"),
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> list[DailyShipmentPoint]:
    return service.daily_shipments(date_from=date_from, date_to=date_to)


@router.get("/deliveries-by-branch", response_model=list[BranchDeliveryPoint])
def deliveries_by_branch(
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> list[BranchDeliveryPoint]:
    return service.deliveries_by_branch()


@router.get("/activity", response_model=list[ActivityItem])
def recent_activity(
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> list[ActivityItem]:
    return service.recent_activity()


@router.get("/summary", response_model=ReportSummary)
def summary(
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> ReportSummary:
    return service.summary()


@router.get("/top-routes", response_model=list[RouteStat])
def top_routes(
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> list[RouteStat]:
    return service.top_routes()


@router.get("/export", response_class=PlainTextResponse, summary="Exportar CSV")
def export_csv(
    format: str = Query(default="csv"),
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> PlainTextResponse:
    if format != "csv":
        return PlainTextResponse("unsupported format", status_code=400)
    return PlainTextResponse(service.export_csv(), media_type="text/csv")
