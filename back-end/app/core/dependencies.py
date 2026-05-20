from functools import lru_cache

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.repositories.branches import InMemoryBranchRepository, SqlAlchemyBranchRepository
from app.repositories.deliveries import InMemoryDeliveryRepository, SqlAlchemyDeliveryRepository
from app.repositories.logistics import InMemoryBatchRepository, InMemoryVehicleRepository, SqlAlchemyBatchRepository, SqlAlchemyVehicleRepository
from app.repositories.notifications import InMemoryNotificationRepository, SqlAlchemyNotificationRepository
from app.repositories.parcels import InMemoryParcelRepository, InMemoryTrackingRepository, SqlAlchemyParcelRepository, SqlAlchemyTrackingRepository
from app.repositories.user_management import InMemoryUserManagementRepository, SqlAlchemyUserManagementRepository
from app.repositories.users import InMemoryUserRepository, SqlAlchemyUserRepository
from app.schemas.user import UserInDB
from app.services.auth import AuthService
from app.services.deliveries import DeliveryService
from app.services.logistics import LogisticsService
from app.services.notifications import NotificationService
from app.services.parcels import ParcelService
from app.services.reports import ReportService
from app.services.branches import BranchService
from app.services.users_management import UserManagementService
from app.services.seed import seed_users
from app.services.seed_branches import seed_branches
from app.services.seed_deliveries import seed_deliveries
from app.services.seed_logistics import seed_batches, seed_vehicles
from app.services.seed_parcels import seed_parcels, seed_tracking_history
from app.services.seed_users_management import seed_users_management


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@lru_cache
def get_user_repository() -> InMemoryUserRepository:
    return InMemoryUserRepository(seed_users())


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(SqlAlchemyUserRepository(db))


@lru_cache
def get_parcel_repository() -> InMemoryParcelRepository:
    return InMemoryParcelRepository(seed_parcels())


@lru_cache
def get_tracking_repository() -> InMemoryTrackingRepository:
    return InMemoryTrackingRepository(seed_tracking_history())


@lru_cache
def get_notification_repository() -> InMemoryNotificationRepository:
    return InMemoryNotificationRepository()


def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(SqlAlchemyNotificationRepository(db))


def get_parcel_service(
    db: AsyncSession = Depends(get_db),
    notifications: NotificationService = Depends(get_notification_service),
) -> ParcelService:
    return ParcelService(SqlAlchemyParcelRepository(db), SqlAlchemyTrackingRepository(db), notifications)


@lru_cache
def get_batch_repository() -> InMemoryBatchRepository:
    return InMemoryBatchRepository(seed_batches())


@lru_cache
def get_vehicle_repository() -> InMemoryVehicleRepository:
    return InMemoryVehicleRepository(seed_vehicles())


def get_logistics_service(
    db: AsyncSession = Depends(get_db),
    notifications: NotificationService = Depends(get_notification_service),
) -> LogisticsService:
    return LogisticsService(SqlAlchemyBatchRepository(db), SqlAlchemyVehicleRepository(db), notifications)


def get_report_service(
    notifications: NotificationService = Depends(get_notification_service),
) -> ReportService:
    return ReportService(notifications)


@lru_cache
def get_branch_repository() -> InMemoryBranchRepository:
    return InMemoryBranchRepository(seed_branches())


def get_branch_service(db: AsyncSession = Depends(get_db)) -> BranchService:
    return BranchService(SqlAlchemyBranchRepository(db))


@lru_cache
def get_user_management_repository() -> InMemoryUserManagementRepository:
    return InMemoryUserManagementRepository(seed_users_management())


def get_user_management_service(db: AsyncSession = Depends(get_db)) -> UserManagementService:
    return UserManagementService(SqlAlchemyUserManagementRepository(db))


@lru_cache
def get_delivery_repository() -> InMemoryDeliveryRepository:
    return InMemoryDeliveryRepository(seed_deliveries())


def get_delivery_service(
    db: AsyncSession = Depends(get_db),
    notifications: NotificationService = Depends(get_notification_service),
) -> DeliveryService:
    return DeliveryService(SqlAlchemyDeliveryRepository(db), notifications)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> UserInDB:
    return await service.get_current_user(token)
