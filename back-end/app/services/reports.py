from __future__ import annotations

from datetime import datetime, timedelta
from io import StringIO
from typing import Optional

from app.repositories.deliveries import DeliveryRepository
from app.repositories.parcels import ParcelRepository
from app.repositories.user_management import UserManagementRepository
from app.schemas.notification import NotificationSchema
from app.schemas.parcel import ParcelStatus
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


class ReportService:
    def __init__(
        self,
        parcels_repo: ParcelRepository,
        deliveries_repo: DeliveryRepository,
        users_repo: UserManagementRepository,
        notifications: Optional[NotificationService] = None,
    ) -> None:
        self._parcels = parcels_repo
        self._deliveries = deliveries_repo
        self._users = users_repo
        self._notifications = notifications

    async def _trend(self, current: int, previous: int) -> int:
        if previous == 0:
            return 100 if current > 0 else 0
        return int(((current - previous) / previous) * 100)

    async def kpis(self, date_from: str | None = None, date_to: str | None = None) -> KPIResponse:
        parcels = await self._parcels.list()
        total = len(parcels)
        in_transit = sum(1 for p in parcels if p.status == ParcelStatus.IN_TRANSIT)
        delivered = sum(1 for p in parcels if p.status == ParcelStatus.DELIVERED)
        returned = sum(1 for p in parcels if p.status == ParcelStatus.RETURNED)

        today_str = datetime.now().strftime("%Y-%m-%d")
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        today_created = [p for p in parcels if p.created_at and p.created_at.startswith(today_str)]
        yesterday_created = [p for p in parcels if p.created_at and p.created_at.startswith(yesterday_str)]
        today_updated = [p for p in parcels if p.updated_at and p.updated_at.startswith(today_str)]
        yesterday_updated = [p for p in parcels if p.updated_at and p.updated_at.startswith(yesterday_str)]

        return KPIResponse(
            totalShipments=total,
            inTransit=in_transit,
            delivered=delivered,
            returned=returned,
            totalShipmentsTrend=await self._trend(len(today_created), len(yesterday_created)),
            inTransitTrend=await self._trend(
                sum(1 for p in today_updated if p.status == ParcelStatus.IN_TRANSIT),
                sum(1 for p in yesterday_updated if p.status == ParcelStatus.IN_TRANSIT),
            ),
            deliveredTrend=await self._trend(
                sum(1 for p in today_updated if p.status == ParcelStatus.DELIVERED),
                sum(1 for p in yesterday_updated if p.status == ParcelStatus.DELIVERED),
            ),
            returnedTrend=await self._trend(
                sum(1 for p in today_updated if p.status == ParcelStatus.RETURNED),
                sum(1 for p in yesterday_updated if p.status == ParcelStatus.RETURNED),
            ),
        )

    async def daily_shipments(self, date_from: str | None = None, date_to: str | None = None) -> list[DailyShipmentPoint]:
        parcels = await self._parcels.list()
        if date_from and date_to:
            start = datetime.strptime(date_from, "%Y-%m-%d")
            end = datetime.strptime(date_to, "%Y-%m-%d")
            days = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
        else:
            today = datetime.now()
            days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        counts = {d: 0 for d in days}
        for p in parcels:
            day = p.created_at[:10] if p.created_at else ""
            if day in counts:
                counts[day] += 1
        return [DailyShipmentPoint(day=d, count=counts[d]) for d in days]

    async def deliveries_by_branch(self) -> list[BranchDeliveryPoint]:
        parcels = await self._parcels.list()
        delivered = [p for p in parcels if p.status == ParcelStatus.DELIVERED]
        branch_counts: dict[str, int] = {}
        for p in delivered:
            branch = p.destination_branch or "Sin sucursal"
            branch_counts[branch] = branch_counts.get(branch, 0) + 1
        return [BranchDeliveryPoint(branch=b, count=c) for b, c in sorted(branch_counts.items(), key=lambda x: -x[1])]

    async def recent_activity(self) -> list[ActivityItem]:
        if self._notifications:
            notifs: list[NotificationSchema] = await self._notifications.list()
            if notifs:
                items = []
                for n in notifs[:10]:
                    user_name = "Sistema"
                    if n.user_id:
                        try:
                            user = await self._users.get(n.user_id)
                            if user:
                                user_name = user.name
                        except Exception:
                            pass
                    items.append(ActivityItem(
                        action=n.text,
                        time=n.time,
                        user=user_name,
                    ))
                return items
        return []

    async def summary(self) -> ReportSummary:
        parcels = await self._parcels.list()
        total = len(parcels)
        delivered = sum(1 for p in parcels if p.status == ParcelStatus.DELIVERED)
        returned = sum(1 for p in parcels if p.status == ParcelStatus.RETURNED)

        success_rate = f"{int((delivered / total) * 100)}%" if total > 0 else "0%"
        return_rate = f"{int((returned / total) * 100)}%" if total > 0 else "0%"

        deliveries = await self._deliveries.list()
        completed = [d for d in deliveries if d.delivery_date]
        if completed:
            total_days = 0
            count = 0
            for d in completed:
                parcel = next((p for p in parcels if p.guide == d.guide), None)
                if parcel and parcel.created_at:
                    try:
                        created = datetime.strptime(parcel.created_at[:10], "%Y-%m-%d")
                        del_date = datetime.strptime(d.delivery_date[:10], "%Y-%m-%d")
                        total_days += (del_date - created).days
                        count += 1
                    except ValueError:
                        pass
            avg_days = round(total_days / count, 1) if count > 0 else 0
            avg_time = f"{avg_days} dias"
        else:
            avg_time = "-"

        return ReportSummary(
            totalVolume=total,
            avgDeliveryTime=avg_time,
            successRate=success_rate,
            returnRate=return_rate,
        )

    async def top_routes(self) -> list[RouteStat]:
        parcels = await self._parcels.list()
        route_counts: dict[str, int] = {}
        for p in parcels:
            route = f"{p.origin_branch} -> {p.destination_branch}"
            route_counts[route] = route_counts.get(route, 0) + 1
        sorted_routes = sorted(route_counts.items(), key=lambda x: -x[1])[:10]
        return [RouteStat(route=r, volume=c, avgTime="-") for r, c in sorted_routes]

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
