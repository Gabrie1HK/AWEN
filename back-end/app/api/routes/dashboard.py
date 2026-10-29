from fastapi import APIRouter, Depends

from app.core.dependencies import get_report_service, require_permission
from app.schemas.reports import DashboardResponse
from app.services.reports import ReportService


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse, summary="Dashboard con KPIS", dependencies=[Depends(require_permission())])
async def dashboard(
    service: ReportService = Depends(get_report_service),
) -> DashboardResponse:
    """Devuelve KPIs, volumen diario, entregas por sucursal y actividad reciente."""
    return await service.get_dashboard()
