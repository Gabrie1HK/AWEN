from __future__ import annotations

from typing import Dict, List

from pydantic import Field

from app.schemas.base import AppBaseModel


class KPIResponse(AppBaseModel):
    total_shipments: int = Field(..., alias="totalShipments")
    in_transit: int = Field(..., alias="inTransit")
    delivered: int
    returned: int


class DailyShipmentPoint(AppBaseModel):
    day: str
    count: int


class BranchDeliveryPoint(AppBaseModel):
    branch: str
    count: int


class ActivityItem(AppBaseModel):
    time: str
    action: str
    user: str


class ReportSummary(AppBaseModel):
    total_volume: int = Field(..., alias="totalVolume")
    avg_delivery_time: str = Field(..., alias="avgDeliveryTime")
    success_rate: str = Field(..., alias="successRate")
    return_rate: str = Field(..., alias="returnRate")


class RouteStat(AppBaseModel):
    route: str
    volume: int
    avg_time: str = Field(..., alias="avgTime")


class StatusBreakdown(AppBaseModel):
    counts: Dict[str, int]


class DashboardResponse(AppBaseModel):
    kpis: KPIResponse
    daily_shipments: List[DailyShipmentPoint] = Field(..., alias="dailyShipments")
    deliveries_by_branch: List[BranchDeliveryPoint] = Field(..., alias="deliveriesByBranch")
    recent_activity: List[ActivityItem] = Field(..., alias="recentActivity")
