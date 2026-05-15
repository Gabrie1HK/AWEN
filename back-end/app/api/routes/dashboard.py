from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_report_service
from app.schemas.reports import DashboardResponse
from app.services.reports import ReportService


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse, summary="Dashboard con KPIS")
def dashboard(
    service: ReportService = Depends(get_report_service),
    _user=Depends(get_current_user),
) -> DashboardResponse:
    """Devuelve KPIs, volumen diario, entregas por sucursal y actividad reciente."""
    return DashboardResponse(
        kpis=service.kpis(),
        dailyShipments=service.daily_shipments(),
        deliveriesByBranch=service.deliveries_by_branch(),
        recentActivity=service.recent_activity(),
    )
