from app.schemas.reports import (
    ActivityItem,
    BranchDeliveryPoint,
    DailyShipmentPoint,
    KPIResponse,
    ReportSummary,
    RouteStat,
)


def seed_dashboard_kpis() -> KPIResponse:
    return KPIResponse(totalShipments=48, inTransit=23, delivered=18, returned=7)


def seed_daily_shipments() -> list[DailyShipmentPoint]:
    return [
        DailyShipmentPoint(day="May 07", count=5),
        DailyShipmentPoint(day="May 08", count=8),
        DailyShipmentPoint(day="May 09", count=6),
        DailyShipmentPoint(day="May 10", count=10),
        DailyShipmentPoint(day="May 11", count=7),
        DailyShipmentPoint(day="May 12", count=9),
        DailyShipmentPoint(day="May 13", count=3),
    ]


def seed_deliveries_by_branch() -> list[BranchDeliveryPoint]:
    return [
        BranchDeliveryPoint(branch="Central", count=18),
        BranchDeliveryPoint(branch="Norte", count=8),
        BranchDeliveryPoint(branch="Sur", count=10),
        BranchDeliveryPoint(branch="Este", count=6),
        BranchDeliveryPoint(branch="Costa", count=4),
        BranchDeliveryPoint(branch="Occidental", count=2),
    ]


def seed_recent_activity() -> list[ActivityItem]:
    return [
        ActivityItem(time="09:15", action="Encomienda AWEN-2026-0001 asignada a ruta", user="Operador Carlos"),
        ActivityItem(time="08:50", action="Conductor Pedro inicia ruta Maracaibo", user="Sistema"),
        ActivityItem(time="08:30", action="Nueva encomienda registrada AWEN-2026-0007", user="Operador Carlos"),
        ActivityItem(time="07:45", action="Entrega confirmada AWEN-2026-0002", user="Conductor Ana"),
        ActivityItem(time="07:00", action="Lote LOT-003 asignado a Conductor Ana", user="Operador Maria"),
    ]


def seed_report_summary() -> ReportSummary:
    return ReportSummary(totalVolume=48, avgDeliveryTime="2.4 dias", successRate="72%", returnRate="15%")


def seed_top_routes() -> list[RouteStat]:
    return [
        RouteStat(route="Central -> Maracaibo", volume=12, avgTime="1.8 dias"),
        RouteStat(route="Central -> Ciudad Guayana", volume=10, avgTime="2.1 dias"),
        RouteStat(route="Este -> Maracay", volume=7, avgTime="1.5 dias"),
        RouteStat(route="Central -> Barquisimeto", volume=5, avgTime="3.5 dias"),
        RouteStat(route="Maracaibo -> Ciudad Guayana", volume=3, avgTime="2.8 dias"),
    ]
