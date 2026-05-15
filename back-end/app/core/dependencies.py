from functools import lru_cache

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.repositories.branches import InMemoryBranchRepository
from app.repositories.deliveries import InMemoryDeliveryRepository
from app.repositories.logistics import InMemoryBatchRepository, InMemoryVehicleRepository
from app.repositories.parcels import InMemoryParcelRepository, InMemoryTrackingRepository
from app.repositories.user_management import InMemoryUserManagementRepository
from app.repositories.users import InMemoryUserRepository
from app.schemas.user import UserInDB
from app.services.auth import AuthService
from app.services.deliveries import DeliveryService
from app.services.logistics import LogisticsService
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


def get_auth_service(repo: InMemoryUserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(repo)


@lru_cache
def get_parcel_repository() -> InMemoryParcelRepository:
    return InMemoryParcelRepository(seed_parcels())


@lru_cache
def get_tracking_repository() -> InMemoryTrackingRepository:
    return InMemoryTrackingRepository(seed_tracking_history())


def get_parcel_service(
    parcels: InMemoryParcelRepository = Depends(get_parcel_repository),
    tracking: InMemoryTrackingRepository = Depends(get_tracking_repository),
) -> ParcelService:
    return ParcelService(parcels, tracking)


@lru_cache
def get_batch_repository() -> InMemoryBatchRepository:
    return InMemoryBatchRepository(seed_batches())


@lru_cache
def get_vehicle_repository() -> InMemoryVehicleRepository:
    return InMemoryVehicleRepository(seed_vehicles())


def get_logistics_service(
    batches: InMemoryBatchRepository = Depends(get_batch_repository),
    vehicles: InMemoryVehicleRepository = Depends(get_vehicle_repository),
) -> LogisticsService:
    return LogisticsService(batches, vehicles)


def get_report_service() -> ReportService:
    return ReportService()


@lru_cache
def get_branch_repository() -> InMemoryBranchRepository:
    return InMemoryBranchRepository(seed_branches())


def get_branch_service(
    branches: InMemoryBranchRepository = Depends(get_branch_repository),
) -> BranchService:
    return BranchService(branches)


@lru_cache
def get_user_management_repository() -> InMemoryUserManagementRepository:
    return InMemoryUserManagementRepository(seed_users_management())


def get_user_management_service(
    users: InMemoryUserManagementRepository = Depends(get_user_management_repository),
) -> UserManagementService:
    return UserManagementService(users)


@lru_cache
def get_delivery_repository() -> InMemoryDeliveryRepository:
    return InMemoryDeliveryRepository(seed_deliveries())


def get_delivery_service(
    deliveries: InMemoryDeliveryRepository = Depends(get_delivery_repository),
) -> DeliveryService:
    return DeliveryService(deliveries)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> UserInDB:
    return service.get_current_user(token)
