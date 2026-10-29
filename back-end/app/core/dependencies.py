from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.repositories.branches import SqlAlchemyBranchRepository
from app.repositories.deliveries import SqlAlchemyDeliveryRepository
from app.repositories.logistics import SqlAlchemyBatchRepository, SqlAlchemyVehicleRepository
from app.repositories.notifications import SqlAlchemyNotificationRepository
from app.repositories.parcels import SqlAlchemyParcelRepository, SqlAlchemyTrackingRepository
from app.repositories.user_management import SqlAlchemyUserManagementRepository
from app.repositories.users import SqlAlchemyUserRepository
from app.schemas.user import UserInDB
from app.services.auth import AuthService
from app.services.deliveries import DeliveryService
from app.services.logistics import LogisticsService
from app.services.notifications import NotificationService
from app.services.parcels import ParcelService
from app.services.reports import ReportService
from app.services.branches import BranchService
from app.services.users_management import UserManagementService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(SqlAlchemyUserRepository(db))


def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(SqlAlchemyNotificationRepository(db))


def get_parcel_service(
    db: AsyncSession = Depends(get_db),
    notifications: NotificationService = Depends(get_notification_service),
) -> ParcelService:
    return ParcelService(
        SqlAlchemyParcelRepository(db),
        SqlAlchemyTrackingRepository(db),
        notifications,
        delivery_repo=SqlAlchemyDeliveryRepository(db),
    )


def get_logistics_service(
    db: AsyncSession = Depends(get_db),
    notifications: NotificationService = Depends(get_notification_service),
) -> LogisticsService:
    return LogisticsService(SqlAlchemyBatchRepository(db), SqlAlchemyVehicleRepository(db), notifications)


def get_report_service(
    db: AsyncSession = Depends(get_db),
    notifications: NotificationService = Depends(get_notification_service),
) -> ReportService:
    return ReportService(
        SqlAlchemyParcelRepository(db),
        SqlAlchemyDeliveryRepository(db),
        SqlAlchemyUserManagementRepository(db),
        notifications,
    )


def get_branch_service(db: AsyncSession = Depends(get_db)) -> BranchService:
    return BranchService(SqlAlchemyBranchRepository(db))


def get_user_management_service(db: AsyncSession = Depends(get_db)) -> UserManagementService:
    return UserManagementService(SqlAlchemyUserManagementRepository(db))


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


def require_permission(method: str = None, path: str = None):
    """
    Dependencia de FastAPI para autorización por rol (RBAC).

    Uso como dependency (no retorna usuario al endpoint):
        @router.get("/endpoint", dependencies=[Depends(require_permission("GET", "/api/v1/endpoint"))])
        async def endpoint(...):
            ...

    Uso como parámetro (retorna usuario al endpoint):
        @router.get("/endpoint")
        async def endpoint(user=Depends(require_permission("GET", "/api/v1/endpoint"))):
            ...

    Args:
        method: Método HTTP del endpoint (solo para documentación, se usa request.method)
        path: Path del endpoint (solo para documentación, se usa request.url.path)
    """
    from fastapi import Request, HTTPException, status
    from app.core.permissions import user_has_permission

    async def _check_permission(request: Request, current_user=Depends(get_current_user)):
        # Verificar si el usuario está activo (R4)
        if not current_user.active:
            from app.core.errors import ForbiddenError
            raise ForbiddenError("Usuario inactivo")

        # Usar SIEMPRE el method y path reales de la request
        # Los argumentos method/path son solo para documentación
        actual_method = request.method
        actual_path = request.url.path

        # Verificar permiso por rol
        if not user_has_permission(current_user.role, actual_method, actual_path):
            from app.core.errors import ForbiddenError
            raise ForbiddenError("No tiene permisos para esta operacion")

        return current_user

    return _check_permission
