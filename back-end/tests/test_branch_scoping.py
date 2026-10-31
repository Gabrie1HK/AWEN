from __future__ import annotations

import io

import pytest
from fastapi.testclient import TestClient
from moto import mock_aws
import boto3


@pytest.fixture
def client_with_branch_scoping(monkeypatch):
    """Cliente con branch scoping y storage mockeado usando moto."""
    # Configurar env vars para storage
    monkeypatch.setenv("AWEN_STORAGE_PROVIDER", "s3")
    monkeypatch.setenv("AWEN_STORAGE_BUCKET", "test-bucket")
    monkeypatch.setenv("AWEN_STORAGE_REGION", "us-east-1")
    monkeypatch.setenv("AWEN_STORAGE_ACCESS_KEY", "test")
    monkeypatch.setenv("AWEN_STORAGE_SECRET_KEY", "test")
    monkeypatch.setenv("AWEN_STORAGE_PRESIGNED_TTL", "3600")
    monkeypatch.setenv("AWEN_UPLOAD_MAX_SIZE", "10485760")
    monkeypatch.setenv("AWEN_UPLOAD_ALLOWED_TYPES", '["image/jpeg","image/png","image/webp","application/pdf"]')
    monkeypatch.setenv("AWEN_SECRET_KEY", "test-secret-key-for-testing-123")

    from app.main import create_app
    from app.core import dependencies
    from app.repositories.users import InMemoryUserRepository
    from app.repositories.parcels import InMemoryParcelRepository, InMemoryTrackingRepository
    from app.repositories.deliveries import InMemoryDeliveryRepository
    from app.repositories.logistics import InMemoryBatchRepository, InMemoryVehicleRepository
    from app.repositories.notifications import InMemoryNotificationRepository
    from app.repositories.branches import InMemoryBranchRepository
    from app.repositories.user_management import InMemoryUserManagementRepository
    from app.services.auth import AuthService
    from app.services.seed import seed_users
    from app.services.seed_deliveries import seed_deliveries
    from app.services.seed_logistics import seed_batches, seed_vehicles
    from app.services.seed_parcels import seed_parcels, seed_tracking_history
    from app.services.seed_branches import seed_branches
    from app.services.seed_users_management import seed_users_management
    from app.services.storage import StorageService
    from app.services.auth import AuthService
    from app.services.deliveries import DeliveryService
    from app.services.logistics import LogisticsService
    from app.services.parcels import ParcelService
    from app.services.notifications import NotificationService
    from app.services.branches import BranchService
    from app.services.users_management import UserManagementService
    from app.services.reports import ReportService
    import boto3

    # Mock AWS con moto
    with mock_aws():
        # Crear bucket en moto
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")

        # Repositorios InMemory
        user_repo = InMemoryUserRepository(seed_users())
        parcel_repo = InMemoryParcelRepository(seed_parcels())
        tracking_repo = InMemoryTrackingRepository(seed_tracking_history())
        delivery_repo = InMemoryDeliveryRepository(seed_deliveries())
        batch_repo = InMemoryBatchRepository(seed_batches())
        vehicle_repo = InMemoryVehicleRepository(seed_vehicles())
        branch_repo = InMemoryBranchRepository(seed_branches())
        user_mgmt_repo = InMemoryUserManagementRepository(seed_users_management())
        notif_repo = InMemoryNotificationRepository()

        # Servicios con repositorios InMemory
        notif_service = NotificationService(notif_repo)
        auth_service = AuthService(user_repo)
        parcel_service = ParcelService(parcel_repo, tracking_repo, notif_service, delivery_repo=InMemoryDeliveryRepository(seed_deliveries()))
        delivery_service = DeliveryService(InMemoryDeliveryRepository(seed_deliveries()), user_repo, None)
        logistics_service = LogisticsService(
            InMemoryBatchRepository(seed_batches()),
            InMemoryVehicleRepository(seed_vehicles()),
            user_repo,
            None
        )
        branch_service = BranchService(InMemoryBranchRepository(seed_branches()))
        user_mgmt_service = UserManagementService(InMemoryUserManagementRepository(seed_users_management()))
        report_service = ReportService(
            InMemoryParcelRepository(seed_parcels()),
            InMemoryDeliveryRepository(seed_deliveries()),
            InMemoryUserManagementRepository(seed_users_management()),
            None
        )
        storage_service = StorageService(
            bucket="test-bucket",
            region="us-east-1",
            access_key="test",
            secret_key="test",
        )

        app = create_app()

        # Override all dependencies
        app.dependency_overrides[dependencies.get_auth_service] = lambda: AuthService(InMemoryUserRepository(seed_users()))
        app.dependency_overrides[dependencies.get_parcel_service] = lambda: ParcelService(
            InMemoryParcelRepository(seed_parcels()),
            InMemoryTrackingRepository(seed_tracking_history()),
            NotificationService(InMemoryNotificationRepository()),
            delivery_repo=InMemoryDeliveryRepository(seed_deliveries())
        )
        app.dependency_overrides[dependencies.get_delivery_service] = lambda: DeliveryService(
            InMemoryDeliveryRepository(seed_deliveries()),
            InMemoryUserRepository(seed_users()),
            None
        )
        app.dependency_overrides[dependencies.get_logistics_service] = lambda: LogisticsService(
            InMemoryBatchRepository(seed_batches()),
            InMemoryVehicleRepository(seed_vehicles()),
            user_repo,
            None
        )
        app.dependency_overrides[dependencies.get_report_service] = lambda: ReportService(
            InMemoryParcelRepository(seed_parcels()),
            InMemoryDeliveryRepository(seed_deliveries()),
            InMemoryUserManagementRepository(seed_users_management()),
            None
        )
        app.dependency_overrides[dependencies.get_branch_service] = lambda: BranchService(InMemoryBranchRepository(seed_branches()))
        app.dependency_overrides[dependencies.get_user_management_service] = lambda: UserManagementService(InMemoryUserManagementRepository(seed_users_management()))
        app.dependency_overrides[dependencies.get_notification_service] = lambda: NotificationService(InMemoryNotificationRepository())
        app.dependency_overrides[dependencies.get_storage_service] = lambda: StorageService(
            bucket="test-bucket",
            region="us-east-1",
            access_key="test",
            secret_key="test",
        )

        with TestClient(app) as c:
            yield c


class TestBranchScoping:
    """Tests para filtrado por sucursal (branch scoping) - Fase 3."""

    def test_parcels_list_filtered_by_operator_branch(self, client_with_branch_scoping, operator_headers):
        """R1: Operator ve solo parcels de su branch (origin O destination)."""
        response = client_with_branch_scoping.get("/api/v1/parcels", headers=operator_headers)
        assert response.status_code == 200
        data = response.json()
        # Operator "Carlos" está en "Sucursal Central"
        for parcel in data.get("data", []):
            assert parcel["originBranch"] == "Sucursal Central" or parcel["destinationBranch"] == "Sucursal Central"

    def test_parcels_list_filtered_by_driver_branch(self, client_with_branch_scoping, driver_headers):
        """R1: Driver ve solo parcels de su branch (origin O destination)."""
        response = client_with_branch_scoping.get("/api/v1/parcels", headers=driver_headers)
        assert response.status_code == 200
        data = response.json()
        # Driver "Pedro" está en "Sucursal Central"
        for parcel in data.get("data", []):
            assert parcel["originBranch"] == "Sucursal Central" or parcel["destinationBranch"] == "Sucursal Central"

    def test_parcels_get_returns_404_for_other_branch(self, client_with_branch_scoping, driver_headers):
        """R7: Driver no puede ver parcel de otro branch (404)."""
        # ENV-004 tiene originBranch="Sucursal Este", destinationBranch="Sucursal Costa"
        # Driver "Pedro" está en "Sucursal Central" -> no debería ver ENV-004
        response = client_with_branch_scoping.get("/api/v1/parcels/ENV-004", headers=driver_headers)
        assert response.status_code == 404

    def test_deliveries_list_filtered_by_driver_branch(self, client_with_branch_scoping, driver_headers):
        """R2: Driver ve solo deliveries de su branch (por driver)."""
        response = client_with_branch_scoping.get("/api/v1/deliveries", headers=driver_headers)
        assert response.status_code == 200
        data = response.json()
        # Driver "Pedro" está en "Sucursal Central"
        # DEL-002 tiene driver="Conductor Pedro" (branch Central)
        # DEL-001 tiene driver="Conductor Ana" (no es Pedro)
        for delivery in data.get("data", []):
            assert delivery["driver"] == "Conductor Pedro"

    def test_deliveries_list_filtered_by_operator_branch(self, client_with_branch_scoping, operator_headers):
        """R2: Operator ve deliveries de drivers de su branch."""
        response = client_with_branch_scoping.get("/api/v1/deliveries", headers=operator_headers)
        assert response.status_code == 200
        data = response.json()
        # Operator "Carlos" en "Sucursal Central"
        # Debe ver deliveries de drivers de "Sucursal Central" (Pedro)
        for delivery in data.get("data", []):
            assert delivery["driver"] in ["Conductor Pedro"]  # Pedro está en Central

    def test_logistics_batches_filtered_by_branch(self, client_with_branch_scoping, operator_headers):
        """R3: Operator ve solo batches de su branch (por driver)."""
        response = client_with_branch_scoping.get("/api/v1/logistics/batches", headers=operator_headers)
        assert response.status_code == 200
        data = response.json()
        # Operator "Carlos" en "Sucursal Central"
        # LOT-001 driver="Conductor Pedro" (Central) -> visible
        # LOT-003 driver="Conductor Ana" (no Central) -> no visible
        for batch in data.get("data", []):
            assert batch["driver"] == "Conductor Pedro"

    def test_logistics_vehicles_filtered_by_branch(self, client_with_branch_scoping, operator_headers):
        """R3: Operator ve solo vehicles de su branch (por driver)."""
        response = client_with_branch_scoping.get("/api/v1/logistics/vehicles", headers=operator_headers)
        assert response.status_code == 200
        data = response.json()
        # Operator "Carlos" en "Sucursal Central"
        # Vehicle ABC-123 driver="Conductor Pedro" (Central) -> visible
        # Vehicle XYZ-789 driver="Conductor Ana" -> no visible
        for vehicle in data.get("data", []):
            assert vehicle["driver"] == "Conductor Pedro"

    def test_users_list_operator_sees_own_branch(self, client_with_branch_scoping, operator_headers):
        """R4: Operator ve solo users de su branch."""
        response = client_with_branch_scoping.get("/api/v1/users", headers=operator_headers)
        assert response.status_code == 200
        data = response.json()
        # Operator "Carlos" en "Sucursal Central"
        for user in data.get("data", []):
            assert user["branch"] == "Sucursal Central"

    def test_reports_kpis_filtered_by_branch(self, client_with_branch_scoping, operator_headers):
        """R5: Reports KPIs filtrados por branch del operator."""
        response = client_with_branch_scoping.get("/api/v1/reports/kpis", headers=operator_headers)
        assert response.status_code == 200
        data = response.json()
        # KPIs deben reflejar solo datos de "Sucursal Central"
        # No verificamos valores exactos, solo que la respuesta es válida
        assert "totalShipments" in data
        assert "inTransit" in data
        assert "delivered" in data
        assert "returned" in data

    def test_dashboard_filtered_by_branch(self, client_with_branch_scoping, operator_headers):
        """R5: Dashboard filtrado por branch del operator."""
        response = client_with_branch_scoping.get("/api/v1/dashboard", headers=operator_headers)
        assert response.status_code == 200
        data = response.json()
        # Dashboard debe tener estructura válida con datos filtrados
        assert "kpis" in data
        assert "dailyShipments" in data
        assert "deliveriesByBranch" in data
        assert "recentActivity" in data

    def test_admin_sees_all_without_filter(self, client_with_branch_scoping, auth_headers):
        """R6: Admin ve todo sin filtro de branch."""
        response = client_with_branch_scoping.get("/api/v1/parcels", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        # Admin ve todas las sucursales
        branches = set()
        for parcel in data.get("data", []):
            branches.add(parcel["originBranch"])
            branches.add(parcel["destinationBranch"])
        # Debe haber al menos 2 sucursales distintas
        assert len(branches) >= 2


class TestBranchScopingSingleResource:
    """Tests para recursos individuales con verificación de ownership/branch."""

    def test_parcels_get_returns_404_for_other_branch_driver(self, client_with_branch_scoping, driver_headers):
        """Driver no puede ver parcel de otro branch."""
        # ENV-004: origin=Sucursal Este, destination=Sucursal Costa
        # Driver Pedro está en Sucursal Central
        response = client_with_branch_scoping.get("/api/v1/parcels/ENV-004", headers=driver_headers)
        assert response.status_code == 404

    def test_parcels_get_returns_404_for_other_branch_operator(self, client_with_branch_scoping, operator_headers):
        """Operator no puede ver parcel de otro branch."""
        # ENV-004: origin=Sucursal Este, destination=Sucursal Costa
        # Operator Carlos está en Sucursal Central
        response = client_with_branch_scoping.get("/api/v1/parcels/ENV-004", headers=operator_headers)
        assert response.status_code == 404

    def test_deliveries_get_returns_404_for_other_branch(self, client_with_branch_scoping, driver_headers):
        """Driver no puede ver delivery de otro driver (distinto branch)."""
        # DEL-001 driver="Conductor Ana" (no es Pedro)
        response = client_with_branch_scoping.get("/api/v1/deliveries/DEL-001", headers=driver_headers)
        assert response.status_code == 404

    def test_logistics_batch_get_returns_404_for_other_branch(self, client_with_branch_scoping, operator_headers):
        """Operator no puede ver batch de driver de otro branch."""
        # LOT-003 driver="Conductor Ana" (no es Central)
        response = client_with_branch_scoping.get("/api/v1/logistics/batches/LOT-003", headers=operator_headers)
        assert response.status_code == 404

    def test_users_get_returns_404_for_other_branch_operator(self, client_with_branch_scoping, operator_headers):
        """Operator no puede ver user de otro branch."""
        # User id=3 (Maria Operador) está en Sucursal Norte
        # Operator Carlos está en Central
        response = client_with_branch_scoping.get("/api/v1/users/3", headers=operator_headers)
        assert response.status_code == 404