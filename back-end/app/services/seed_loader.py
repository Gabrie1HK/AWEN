from __future__ import annotations

import asyncio
from app.database.database import AsyncSessionLocal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.batch import Batch
from app.models.batch_parcel import BatchParcel
from app.models.branch import Branch
from app.models.delivery import Delivery
from app.models.notification import Notification
from app.models.parcel import Parcel
from app.models.tracking_event import TrackingEvent
from app.core.security import get_password_hash
from app.models.user import User
from app.models.user_management import UserManagement
from app.models.vehicle import Vehicle
from app.services.seed import seed_users
from app.services.seed_branches import seed_branches
from app.services.seed_deliveries import seed_deliveries
from app.services.seed_logistics import seed_batches, seed_vehicles
from app.services.seed_parcels import seed_parcels, seed_tracking_history
from app.services.seed_users_management import seed_users_management
from app.services.seed_additional_clients import seed_additional_clients_users, seed_additional_clients_management
from app.services.seed_additional_parcels import seed_additional_parcels
from app.services.seed_additional_deliveries import seed_additional_deliveries
from app.services.seed_additional_tracking import seed_additional_tracking


async def seed_all(session: AsyncSession) -> None:
    await _seed_users(session)
    await _seed_users_management(session)
    await _seed_additional_clients(session)
    await _seed_additional_clients_management(session)
    await _seed_branches(session)
    await _seed_parcels(session)
    await _seed_additional_parcels(session)
    await _seed_tracking(session)
    await _seed_additional_tracking(session)
    await _seed_vehicles(session)
    await _seed_batches(session)
    await _seed_deliveries(session)
    await _seed_additional_deliveries(session)
    await _seed_notifications(session)
    await session.commit()


async def _seed_users(session: AsyncSession) -> None:
    existing = await session.execute(select(User.id))
    if existing.first():
        return
    for i, item in enumerate(seed_users()):
        session.add(
            User(
                id=item.id,
                name=item.name,
                last_name=item.last_name,
                ci=item.ci,
                email=item.email,
                role=item.role,
                branch=item.branch,
                phone=item.phone,
                address=item.address,
                active=item.active,
                hashed_password=item.hashed_password,
                client_number=getattr(item, 'client_number', None) or (1000 + i)  # <--- FIX HERE
            )
        )


async def _seed_additional_clients(session: AsyncSession) -> None:
    existing = await session.execute(select(User.id).where(User.id >= 8))
    if existing.first():
        return
    for item in seed_additional_clients_users():
        session.add(
            User(
                id=item.id,
                name=item.name,
                last_name=item.last_name,
                ci=item.ci,
                email=item.email,
                role=item.role,
                branch=item.branch,
                phone=item.phone,
                address=item.address,
                active=item.active,
                client_number=item.client_number,
                hashed_password=item.hashed_password,
            )
        )


async def _seed_additional_clients_management(session: AsyncSession) -> None:
    existing = await session.execute(select(UserManagement.id).where(UserManagement.id >= 8))
    if existing.first():
        return
    for item in seed_additional_clients_management():
        session.add(
            UserManagement(
                id=item.id,
                name=item.name,
                last_name=item.last_name,
                ci=item.ci,
                email=item.email,
                role=item.role.value,
                branch=item.branch,
                phone=item.phone,
                address=item.address,
                active=item.active,
                last_login=item.last_login,
                hashed_password=get_password_hash("123456"),
            )
        )


async def _seed_additional_parcels(session: AsyncSession) -> None:
    existing = await session.execute(select(Parcel.id).where(Parcel.id >= "ENV-008"))
    if existing.first():
        return
    for item in seed_additional_parcels():
        session.add(
            Parcel(
                id=item.id,
                guide=item.guide,
                sender=item.sender,
                sender_id=item.sender_id,
                sender_phone=item.sender_phone,
                recipient=item.recipient,
                recipient_id=item.recipient_id,
                recipient_phone=item.recipient_phone,
                recipient_address=item.recipient_address,
                origin_address=item.origin_address,
                origin_lat=item.origin_lat,
                origin_lng=item.origin_lng,
                destination_address=item.destination_address,
                destination_lat=item.destination_lat,
                destination_lng=item.destination_lng,
                origin_branch=item.origin_branch,
                destination_branch=item.destination_branch,
                weight=item.weight,
                dimensions=item.dimensions,
                declared_value=item.declared_value,
                description=item.description,
                status=item.status.value,
                created_at=item.created_at,
                updated_at=item.updated_at,
                qr_data=item.qr_data,
                barcode=item.barcode,
            )
        )


async def _seed_users_management(session: AsyncSession) -> None:
    existing = await session.execute(select(UserManagement.id))
    if existing.first():
        return
    for i, item in enumerate(seed_users_management()):
        session.add(
            UserManagement(
                id=item.id,
                name=item.name,
                last_name=item.last_name,
                ci=item.ci,
                email=item.email,
                role=item.role.value,
                branch=item.branch,
                phone=item.phone,
                address=item.address,
                active=item.active,
                last_login=item.last_login,
                hashed_password=get_password_hash("123456"),
                # Add this line if UserManagement also throws a null constraint error:
                # client_number=getattr(item, 'client_number', None) or (5000 + i)
            )
        )


async def _seed_branches(session: AsyncSession) -> None:
    existing = await session.execute(select(Branch.id))
    if existing.first():
        return
    for item in seed_branches():
        session.add(
            Branch(
                id=item.id,
                name=item.name,
                city=item.city,
                address=item.address,
                manager=item.manager,
                phone=item.phone,
                active=item.active,
            )
        )


async def _seed_parcels(session: AsyncSession) -> None:
    existing = await session.execute(select(Parcel.id))
    if existing.first():
        return
    for item in seed_parcels():
        session.add(
            Parcel(
                id=item.id,
                guide=item.guide,
                sender=item.sender,
                sender_id=item.sender_id,
                sender_phone=item.sender_phone,
                recipient=item.recipient,
                recipient_id=item.recipient_id,
                recipient_phone=item.recipient_phone,
                recipient_address=item.recipient_address,
                origin_address=item.origin_address,
                origin_lat=item.origin_lat,
                origin_lng=item.origin_lng,
                destination_address=item.destination_address,
                destination_lat=item.destination_lat,
                destination_lng=item.destination_lng,
                origin_branch=item.origin_branch,
                destination_branch=item.destination_branch,
                weight=item.weight,
                dimensions=item.dimensions,
                declared_value=item.declared_value,
                description=item.description,
                status=item.status.value,
                created_at=item.created_at,
                updated_at=item.updated_at,
                qr_data=item.qr_data,
                barcode=item.barcode,
            )
        )


async def _seed_tracking(session: AsyncSession) -> None:
    existing = await session.execute(select(TrackingEvent.id))
    if existing.first():
        return
    history = seed_tracking_history()
    for guide, events in history.items():
        for item in events:
            session.add(
                TrackingEvent(
                    guide=guide,
                    step=item.step.value,
                    date=item.date,
                    time=item.time,
                    location=item.location,
                    lat=item.lat,
                    lng=item.lng,
                    operator=item.operator,
                    completed=item.completed,
                )
            )


async def _seed_additional_tracking(session: AsyncSession) -> None:
    history = seed_additional_tracking()
    for guide, events in history.items():
        existing = await session.execute(select(TrackingEvent.id).where(TrackingEvent.guide == guide))
        if existing.first():
            continue
        for item in events:
            session.add(
                TrackingEvent(
                    guide=guide,
                    step=item.step.value,
                    date=item.date,
                    time=item.time,
                    location=item.location,
                    lat=item.lat,
                    lng=item.lng,
                    operator=item.operator,
                    completed=item.completed,
                )
            )


async def _seed_vehicles(session: AsyncSession) -> None:
    existing = await session.execute(select(Vehicle.id))
    if existing.first():
        return
    for item in seed_vehicles():
        session.add(
            Vehicle(
                id=item.id,
                plate=item.plate,
                model=item.model,
                capacity=item.capacity,
                driver=item.driver,
            )
        )


async def _seed_batches(session: AsyncSession) -> None:
    existing = await session.execute(select(Batch.id))
    if existing.first():
        return
    for item in seed_batches():
        session.add(
            Batch(
                id=item.id,
                status=item.status.value,
                vehicle=item.vehicle,
                driver=item.driver,
                driver_id=item.driver_id,
                parcel_count=item.parcel_count,
            )
        )
        for parcel_id in item.parcels:
            session.add(BatchParcel(batch_id=item.id, parcel_id=parcel_id))


async def _seed_deliveries(session: AsyncSession) -> None:
    existing = await session.execute(select(Delivery.id))
    if existing.first():
        return
    for item in seed_deliveries():
        session.add(
            Delivery(
                id=item.id,
                guide=item.guide,
                recipient=item.recipient,
                driver=item.driver,
                delivery_date=item.delivery_date,
                pod_type=item.pod_type.value,
                status=item.status.value,
                signature_data=item.signature_data,
                photo_url=item.photo_url,
                gps=item.gps,
            )
        )


async def _seed_additional_deliveries(session: AsyncSession) -> None:
    existing = await session.execute(select(Delivery.id).where(Delivery.id >= "DEL-004"))
    if existing.first():
        return
    for item in seed_additional_deliveries():
        session.add(
            Delivery(
                id=item.id,
                guide=item.guide,
                recipient=item.recipient,
                driver=item.driver,
                delivery_date=item.delivery_date,
                pod_type=item.pod_type.value,
                status=item.status.value,
                signature_data=item.signature_data,
                photo_url=item.photo_url,
                gps=item.gps,
            )
        )


async def _seed_notifications(session: AsyncSession) -> None:
    existing = await session.execute(select(Notification.id))
    if existing.first():
        return
    

async def run_seeding():
    async with AsyncSessionLocal() as session:
        print("Starting seeding process...")
        await seed_all(session)
        print("Seeding complete! Database is now populated.")

if __name__ == "__main__":
    asyncio.run(run_seeding())
