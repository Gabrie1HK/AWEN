from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure app is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from app.core import dependencies
from app.main import create_app
from app.repositories.branches import InMemoryBranchRepository
from app.repositories.deliveries import InMemoryDeliveryRepository
from app.repositories.logistics import InMemoryBatchRepository, InMemoryVehicleRepository
from app.repositories.notifications import InMemoryNotificationRepository
from app.repositories.parcels import InMemoryParcelRepository, InMemoryTrackingRepository
from app.repositories.user_management import InMemoryUserManagementRepository
from app.repositories.users import InMemoryUserRepository
from app.services.auth import AuthService
from app.services.branches import BranchService
from app.services.deliveries import DeliveryService
from app.services.logistics import LogisticsService
from app.services.notifications import NotificationService
from app.services.parcels import ParcelService
from app.services.reports import ReportService
from app.services.users_management import UserManagementService
from app.services.seed import seed_users
from app.services.seed_branches import seed_branches
from app.services.seed_deliveries import seed_deliveries
from app.services.seed_logistics import seed_batches, seed_vehicles
from app.services.seed_parcels import seed_parcels, seed_tracking_history
from app.services.seed_users_management import seed_users_management


@pytest.fixture
def client():
    app = create_app()

    # Override all service dependencies to use in-memory repos (test isolation)
    user_repo = InMemoryUserRepository(seed_users())
    parcel_repo = InMemoryParcelRepository(seed_parcels())
    tracking_repo = InMemoryTrackingRepository(seed_tracking_history())
    branch_repo = InMemoryBranchRepository(seed_branches())
    batch_repo = InMemoryBatchRepository(seed_batches())
    vehicle_repo = InMemoryVehicleRepository(seed_vehicles())
    delivery_repo = InMemoryDeliveryRepository(seed_deliveries())
    user_mgmt_repo = InMemoryUserManagementRepository(seed_users_management())
    notif_repo = InMemoryNotificationRepository()
    notif_service = NotificationService(notif_repo)

    app.dependency_overrides.update({
        dependencies.get_auth_service: lambda: AuthService(user_repo),
        dependencies.get_notification_service: lambda: notif_service,
        dependencies.get_parcel_service: lambda: ParcelService(parcel_repo, tracking_repo, notif_service),
        dependencies.get_logistics_service: lambda: LogisticsService(batch_repo, vehicle_repo, notif_service),
        dependencies.get_report_service: lambda: ReportService(notif_service),
        dependencies.get_branch_service: lambda: BranchService(branch_repo),
        dependencies.get_user_management_service: lambda: UserManagementService(user_mgmt_repo),
        dependencies.get_delivery_service: lambda: DeliveryService(delivery_repo, notif_service),
    })

    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_token(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@awen.com", "password": "123456"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
