from app.schemas.notification import NotificationSchema
from datetime import datetime, timezone


def seed_notifications() -> list[NotificationSchema]:
    """Seed sample notifications for reports activity."""
    now = datetime.now(timezone.utc)
    return [
        NotificationSchema(
            id=str(int(now.timestamp() * 1000)),
            user_id=2,
            text="Encomienda AWEN-2026-0001 creada",
            action_type="parcel_created",
            related_id="ENV-001",
            time=now.strftime("%H:%M"),
            created_at=now.isoformat(),
            read=False,
        ),
        NotificationSchema(
            id=str(int((now.timestamp() + 1) * 1000)),
            user_id=4,
            text="Entrega ENV-001 completada con POD",
            action_type="delivery_completed",
            related_id="DEL-001",
            time=now.strftime("%H:%M"),
            created_at=now.isoformat(),
            read=False,
        ),
        NotificationSchema(
            id=str(int((now.timestamp() + 2) * 1000)),
            user_id=2,
            text="Lote LOT-001 asignado a vehiculo ABC-123",
            action_type="batch_assigned",
            related_id="LOT-001",
            time=now.strftime("%H:%M"),
            created_at=now.isoformat(),
            read=False,
        ),
    ]