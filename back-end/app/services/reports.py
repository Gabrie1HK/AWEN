from __future__ import annotations

from io import StringIO
from typing import Optional

from app.schemas.notification import NotificationSchema
from app.schemas.reports import (
    ActivityItem,
    BranchDeliveryPoint,
    DashboardResponse,
    DailyShipmentPoint,
    KPIResponse,
    ReportSummary,
    RouteStat,
)
from app.services.notifications import NotificationService
from app.services.seed_reports import (
    seed_dashboard_kpis,
    seed_daily_shipments,
    seed_deliveries_by_branch,
    seed_recent_activity,
    seed_report_summary,
    seed_top_routes,
)


class ReportService:
    def __init__(self, notifications: Optional[NotificationService] = None) -> None:
        self._notifications = notifications

    async def kpis(self, date_from: str | None = None, date_to: str | None = None) -> KPIResponse:
        return seed_dashboard_kpis()

    async def daily_shipments(self, date_from: str | None = None, date_to: str | None = None) -> list[DailyShipmentPoint]:
        return seed_daily_shipments()

    async def deliveries_by_branch(self) -> list[BranchDeliveryPoint]:
        return seed_deliveries_by_branch()

    async def recent_activity(self) -> list[ActivityItem]:
        if self._notifications:
            notifs: list[NotificationSchema] = await self._notifications.list()
            if notifs:
                return [
                    ActivityItem(
                        action=n.text,
                        time=n.time,
                        user=n.action_type,
                    )
                    for n in notifs[:10]
                ]
        return seed_recent_activity()

    async def summary(self) -> ReportSummary:
        return seed_report_summary()

    async def top_routes(self) -> list[RouteStat]:
        return seed_top_routes()

    async def export_csv(self) -> str:
        buffer = StringIO()
        buffer.write("route,volume,avg_time\n")
        for item in await self.top_routes():
            buffer.write(f"{item.route},{item.volume},{item.avg_time}\n")
        return buffer.getvalue()

    async def get_dashboard(self) -> DashboardResponse:
        return DashboardResponse(
            kpis=await self.kpis(),
            dailyShipments=await self.daily_shipments(),
            deliveriesByBranch=await self.deliveries_by_branch(),
            recentActivity=await self.recent_activity(),
        )
