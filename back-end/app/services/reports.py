from __future__ import annotations

from io import StringIO

from app.schemas.reports import (
    ActivityItem,
    BranchDeliveryPoint,
    DailyShipmentPoint,
    KPIResponse,
    ReportSummary,
    RouteStat,
)
from app.services.seed_reports import (
    seed_dashboard_kpis,
    seed_daily_shipments,
    seed_deliveries_by_branch,
    seed_recent_activity,
    seed_report_summary,
    seed_top_routes,
)


class ReportService:
    def kpis(self, date_from: str | None = None, date_to: str | None = None) -> KPIResponse:
        return seed_dashboard_kpis()

    def daily_shipments(self, date_from: str | None = None, date_to: str | None = None) -> list[DailyShipmentPoint]:
        return seed_daily_shipments()

    def deliveries_by_branch(self) -> list[BranchDeliveryPoint]:
        return seed_deliveries_by_branch()

    def recent_activity(self) -> list[ActivityItem]:
        return seed_recent_activity()

    def summary(self) -> ReportSummary:
        return seed_report_summary()

    def top_routes(self) -> list[RouteStat]:
        return seed_top_routes()

    def export_csv(self) -> str:
        buffer = StringIO()
        buffer.write("route,volume,avg_time\n")
        for item in self.top_routes():
            buffer.write(f"{item.route},{item.volume},{item.avg_time}\n")
        return buffer.getvalue()
