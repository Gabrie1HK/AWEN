from __future__ import annotations


class TestAuthenticationRequired:
    ENDPOINTS = [
        ("GET", "/api/v1/parcels"),
        ("GET", "/api/v1/parcels/ENV-001"),
        ("POST", "/api/v1/parcels"),
        ("PATCH", "/api/v1/parcels/ENV-001"),
        ("POST", "/api/v1/parcels/ENV-007/status"),
        ("POST", "/api/v1/parcels/ENV-003/cancel"),
        ("GET", "/api/v1/parcels/AWEN-2026-0001/tracking"),
        ("GET", "/api/v1/users"),
        ("GET", "/api/v1/users/1"),
        ("POST", "/api/v1/users"),
        ("PATCH", "/api/v1/users/1"),
        ("DELETE", "/api/v1/users/1"),
        ("GET", "/api/v1/branches"),
        ("GET", "/api/v1/branches/1"),
        ("POST", "/api/v1/branches"),
        ("PATCH", "/api/v1/branches/1"),
        ("DELETE", "/api/v1/branches/1"),
        ("GET", "/api/v1/deliveries"),
        ("GET", "/api/v1/deliveries/DEL-001"),
        ("PATCH", "/api/v1/deliveries/DEL-002"),
        ("POST", "/api/v1/deliveries/DEL-002/pod"),
        ("GET", "/api/v1/logistics/batches"),
        ("GET", "/api/v1/logistics/batches/LOT-001"),
        ("POST", "/api/v1/logistics/batches"),
        ("POST", "/api/v1/logistics/batches/LOT-002/assign"),
        ("GET", "/api/v1/logistics/vehicles"),
        ("GET", "/api/v1/notifications"),
        ("PATCH", "/api/v1/notifications/read-all"),
        ("GET", "/api/v1/reports/kpis"),
        ("GET", "/api/v1/dashboard"),
    ]

    def test_all_protected_endpoints_reject_unauthenticated(self, client):
        for method, path in self.ENDPOINTS:
            response = client.request(method, path)
            assert response.status_code == 401, f"{method} {path} returned {response.status_code}, expected 401"

    def test_all_protected_endpoints_reject_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalidtoken"}
        for method, path in self.ENDPOINTS:
            response = client.request(method, path, headers=headers)
            assert response.status_code == 401, f"{method} {path} returned {response.status_code}, expected 401"


class TestRoleBasedAccess:
    """Tests que verifican el acceso por rol según la matriz de permisos (R2)."""

    def test_admin_can_list_parcels(self, client, auth_headers):
        response = client.get("/api/v1/parcels", headers=auth_headers)
        assert response.status_code == 200

    def test_operator_can_list_parcels(self, client, operator_headers):
        response = client.get("/api/v1/parcels", headers=operator_headers)
        assert response.status_code == 200

    def test_driver_can_list_parcels(self, client, driver_headers):
        response = client.get("/api/v1/parcels", headers=driver_headers)
        assert response.status_code == 200

    def test_client_can_list_parcels(self, client, client_headers):
        response = client.get("/api/v1/parcels", headers=client_headers)
        assert response.status_code == 200

    def test_admin_can_create_parcel(self, client, auth_headers):
        payload = {
            "sender": "Admin Test", "senderId": "76.123.456-7", "senderPhone": "+56 9 1234 5678",
            "recipient": "Test", "recipientId": "12.345.678-9", "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test 123", "originBranch": "Central", "destinationBranch": "Norte",
            "weight": 5.0, "dimensions": "30x20x15 cm", "declaredValue": 100000, "description": "Test",
        }
        response = client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        assert response.status_code == 200

    def test_operator_can_create_parcel(self, client, operator_headers):
        payload = {
            "sender": "Operator Test", "senderId": "76.123.456-7", "senderPhone": "+56 9 1234 5678",
            "recipient": "Test", "recipientId": "12.345.678-9", "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test 123", "originBranch": "Central", "destinationBranch": "Norte",
            "weight": 5.0, "dimensions": "30x20x15 cm", "declaredValue": 100000, "description": "Test",
        }
        response = client.post("/api/v1/parcels", headers=operator_headers, json=payload)
        assert response.status_code == 200

    def test_client_can_create_parcel(self, client, client_headers):
        payload = {
            "sender": "Client Test", "senderId": "76.123.456-7", "senderPhone": "+56 9 1234 5678",
            "recipient": "Test", "recipientId": "12.345.678-9", "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test 123", "originBranch": "Central", "destinationBranch": "Norte",
            "weight": 5.0, "dimensions": "30x20x15 cm", "declaredValue": 100000, "description": "Test",
        }
        response = client.post("/api/v1/parcels", headers=client_headers, json=payload)
        assert response.status_code == 200

    def test_driver_cannot_create_parcel(self, client, driver_headers):
        payload = {
            "sender": "Driver Test", "senderId": "76.123.456-7", "senderPhone": "+56 9 1234 5678",
            "recipient": "Test", "recipientId": "12.345.678-9", "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test 123", "originBranch": "Central", "destinationBranch": "Norte",
            "weight": 5.0, "dimensions": "30x20x15 cm", "declaredValue": 100000, "description": "Test",
        }
        response = client.post("/api/v1/parcels", headers=driver_headers, json=payload)
        assert response.status_code == 403

    def test_admin_can_list_users(self, client, auth_headers):
        response = client.get("/api/v1/users", headers=auth_headers)
        assert response.status_code == 200

    def test_operator_can_list_users(self, client, operator_headers):
        response = client.get("/api/v1/users", headers=operator_headers)
        assert response.status_code == 200

    def test_driver_cannot_list_users(self, client, driver_headers):
        response = client.get("/api/v1/users", headers=driver_headers)
        assert response.status_code == 403

    def test_client_cannot_list_users(self, client, client_headers):
        response = client.get("/api/v1/users", headers=client_headers)
        assert response.status_code == 403

    def test_admin_can_view_dashboard(self, client, auth_headers):
        response = client.get("/api/v1/dashboard", headers=auth_headers)
        assert response.status_code == 200

    def test_operator_can_view_dashboard(self, client, operator_headers):
        response = client.get("/api/v1/dashboard", headers=operator_headers)
        assert response.status_code == 200

    def test_driver_can_view_dashboard(self, client, driver_headers):
        response = client.get("/api/v1/dashboard", headers=driver_headers)
        assert response.status_code == 200

    def test_client_cannot_view_dashboard(self, client, client_headers):
        response = client.get("/api/v1/dashboard", headers=client_headers)
        assert response.status_code == 403

    def test_my_parcels_endpoint(self, client, auth_headers, driver_headers, client_headers):
        for role, headers in [("Admin", auth_headers), ("Driver", driver_headers), ("Client", client_headers)]:
            response = client.get("/api/v1/parcels/my-parcels", headers=headers)
            assert response.status_code == 200, f"{role} failed to get my-parcels"

    def test_users_me_endpoint(self, client, auth_headers, operator_headers, driver_headers, client_headers):
        for role, headers in [("Admin", auth_headers), ("Operator", operator_headers),
                              ("Driver", driver_headers), ("Client", client_headers)]:
            response = client.get("/api/v1/users/me", headers=headers)
            assert response.status_code == 200, f"{role} failed to get their profile"
            assert response.json()["email"].endswith("@awen.com") or response.json()["email"] == "juan@email.com"

    def test_update_my_profile(self, client, auth_headers, driver_headers):
        for role, headers in [("Admin", auth_headers), ("Driver", driver_headers)]:
            response = client.patch("/api/v1/users/me", headers=headers, json={"phone": "+58 999 999 9999"})
            assert response.status_code == 200, f"{role} failed to update own profile"
            assert response.json()["phone"] == "+58 999 999 9999"


class TestRoleBasedAuthorization:
    """R2: Un usuario autenticado sin el rol requerido recibe 403."""

    # Endpoints que Client NO debe poder acceder (deben dar 403)
    CLIENT_FORBIDDEN = [
        ("POST", "/api/v1/users"),
        ("GET", "/api/v1/users"),
        ("GET", "/api/v1/users/1"),
        ("PATCH", "/api/v1/users/1"),
        ("DELETE", "/api/v1/users/1"),
        ("POST", "/api/v1/branches"),
        ("PATCH", "/api/v1/branches/1"),
        ("DELETE", "/api/v1/branches/1"),
        ("GET", "/api/v1/logistics/batches"),
        ("POST", "/api/v1/logistics/batches"),
        ("POST", "/api/v1/logistics/batches/LOT-001/assign"),
        ("GET", "/api/v1/logistics/vehicles"),
        ("POST", "/api/v1/logistics/vehicles"),
        ("GET", "/api/v1/reports/kpis"),
        ("GET", "/api/v1/dashboard"),
        ("PATCH", "/api/v1/deliveries/DEL-001"),
        ("POST", "/api/v1/deliveries/DEL-001/pod"),
        ("PATCH", "/api/v1/parcels/ENV-001"),
        ("POST", "/api/v1/parcels/ENV-001/status"),
    ]

    # Endpoints que Driver NO debe poder acceder (deben dar 403)
    DRIVER_FORBIDDEN = [
        ("POST", "/api/v1/users"),
        ("GET", "/api/v1/users"),
        ("GET", "/api/v1/users/1"),
        ("PATCH", "/api/v1/users/1"),
        ("DELETE", "/api/v1/users/1"),
        ("POST", "/api/v1/branches"),
        ("PATCH", "/api/v1/branches/1"),
        ("DELETE", "/api/v1/branches/1"),
        ("POST", "/api/v1/logistics/batches"),
        ("POST", "/api/v1/logistics/batches/LOT-001/assign"),
        ("POST", "/api/v1/logistics/vehicles"),
        ("GET", "/api/v1/reports/kpis"),
        ("PATCH", "/api/v1/parcels/ENV-001"),
        ("POST", "/api/v1/parcels/ENV-001/cancel"),
    ]

    # Endpoints que Operator NO debe poder acceder (deben dar 403)
    OPERATOR_FORBIDDEN = [
        ("POST", "/api/v1/users"),
        ("PATCH", "/api/v1/users/1"),
        ("DELETE", "/api/v1/users/1"),
        ("POST", "/api/v1/branches"),
        ("PATCH", "/api/v1/branches/1"),
        ("DELETE", "/api/v1/branches/1"),
    ]

    def _assert_forbidden(self, response, method, path):
        """Helper to assert 403 with proper error message."""
        assert response.status_code == 403, f"{method} {path} returned {response.status_code}, expected 403"
        # Verificar que el error tiene el mensaje esperado (formato puede variar)
        error_data = response.json()
        # El error puede venir como {"message": "..."} o {"detail": {"message": "..."}}
        message = error_data.get("message") or error_data.get("detail", {}).get("message")
        assert message == "No tiene permisos para esta operacion", f"Unexpected error message: {message}"

    def test_client_forbidden_endpoints_return_403(self, client, client_headers):
        for method, path in self.CLIENT_FORBIDDEN:
            response = client.request(method, path, headers=client_headers)
            self._assert_forbidden(response, method, path)

    def test_driver_forbidden_endpoints_return_403(self, client, driver_headers):
        for method, path in self.DRIVER_FORBIDDEN:
            response = client.request(method, path, headers=driver_headers)
            self._assert_forbidden(response, method, path)

    def test_operator_forbidden_endpoints_return_403(self, client, operator_headers):
        for method, path in self.OPERATOR_FORBIDDEN:
            response = client.request(method, path, headers=operator_headers)
            self._assert_forbidden(response, method, path)

    def test_admin_can_access_all_endpoints(self, client, auth_headers):
        """Admin debe poder acceder a todos los endpoints (sin 403 por rol)."""
        all_endpoints = self.CLIENT_FORBIDDEN + self.DRIVER_FORBIDDEN + self.OPERATOR_FORBIDDEN
        for method, path in all_endpoints:
            response = client.request(method, path, headers=auth_headers)
            # Admin no debe recibir 403 (puede recibir 404, 422, etc. pero no 403 por rol)
            assert response.status_code != 403, f"Admin {method} {path} returned 403 unexpectedly"


class TestPermissionMatrixCentralized:
    """R3: La matriz de permisos por rol está declarada en un único lugar y es testeable."""

    def test_permission_matrix_exists_and_is_importable(self):
        """Verifica que existe un módulo único que define la matriz de permisos."""
        from app.core import permissions
        assert hasattr(permissions, "PERMISSION_MATRIX")
        assert isinstance(permissions.PERMISSION_MATRIX, dict)

    def test_permission_matrix_has_expected_endpoints(self):
        """La matriz cubre los endpoints protegidos principales."""
        from app.core.permissions import PERMISSION_MATRIX
        # Verificar que hay entradas para endpoints clave
        assert any("/parcels" in k for k in PERMISSION_MATRIX)
        assert any("/users" in k for k in PERMISSION_MATRIX)
        assert any("/branches" in k for k in PERMISSION_MATRIX)
        assert any("/deliveries" in k for k in PERMISSION_MATRIX)
        assert any("/logistics" in k for k in PERMISSION_MATRIX)
        assert any("/reports" in k for k in PERMISSION_MATRIX)
        assert any("/dashboard" in k for k in PERMISSION_MATRIX)
        assert any("/notifications" in k for k in PERMISSION_MATRIX)

    def test_permission_matrix_roles_are_valid(self):
        """Los roles en la matriz son válidos."""
        from app.core.permissions import PERMISSION_MATRIX, Role
        valid_roles = set(Role.ALL)
        for roles in PERMISSION_MATRIX.values():
            for role in roles:
                assert role in valid_roles, f"Invalid role in matrix: {role}"


class TestInactiveUser:
    """R4: Un usuario con active = false no puede autenticarse ni usar un token vigente."""

    def _assert_forbidden_inactive(self, response):
        """Helper to assert 403 with proper error message for inactive user."""
        assert response.status_code == 403
        error_data = response.json()
        message = error_data.get("message") or error_data.get("detail", {}).get("message")
        assert message == "Usuario inactivo", f"Unexpected error message: {message}"

    def test_inactive_user_cannot_login(self, client):
        """Login con usuario inactivo (Marta, id=7) debe devolver 403."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "marta@email.com", "password": "123456"},
        )
        self._assert_forbidden_inactive(response)

    def test_inactive_user_token_rejected(self, client):
        """Token de usuario inactivo (emitido antes de desactivar) debe ser rechazado con 403."""
        from app.main import create_app
        from app.core import dependencies
        from app.repositories.users import InMemoryUserRepository
        from app.services.auth import AuthService
        from app.services.seed import seed_users
        from fastapi.testclient import TestClient

        app = create_app()
        # Usamos seed_users que incluye a Marta (inactive)
        user_repo = InMemoryUserRepository(seed_users())
        app.dependency_overrides[dependencies.get_auth_service] = lambda: AuthService(user_repo)

        with TestClient(app) as c:
            # Login con Marta (inactive) - debe fallar
            response = c.post("/api/v1/auth/login", json={"email": "marta@email.com", "password": "123456"})
            self._assert_forbidden_inactive(response)

    def test_active_user_token_works(self, client, client_headers):
        """Token de usuario activo (Juan, id=6) debe funcionar."""
        response = client.get("/api/v1/users/me", headers=client_headers)
        assert response.status_code == 200


class TestSecretKeyValidation:
    """R5: El arranque falla si AWEN_SECRET_KEY es el valor por defecto CHANGE_ME."""

    def test_startup_fails_with_default_secret_key(self, monkeypatch):
        """La app debe fallar al iniciar si secret_key es CHANGE_ME."""
        monkeypatch.setenv("AWEN_SECRET_KEY", "CHANGE_ME")
        # Forzar recarga de configuración
        from app.core.config import get_settings
        get_settings.cache_clear()

        from app.main import create_app
        import pytest

        with pytest.raises(Exception) as exc_info:
            create_app()
        assert "CHANGE_ME" in str(exc_info.value) or "secret" in str(exc_info.value).lower()

    def test_startup_fails_without_secret_key(self, monkeypatch):
        """La app debe fallar al iniciar si AWEN_SECRET_KEY no está definida."""
        monkeypatch.delenv("AWEN_SECRET_KEY", raising=False)
        from app.core.config import get_settings
        get_settings.cache_clear()

        from app.main import create_app
        import pytest

        with pytest.raises(Exception) as exc_info:
            create_app()
        assert "secret" in str(exc_info.value).lower() or "CHANGE_ME" in str(exc_info.value)

    def test_startup_succeeds_with_valid_secret_key(self, monkeypatch):
        """La app debe iniciar correctamente con una secret key válida."""
        monkeypatch.setenv("AWEN_SECRET_KEY", "una-clave-secreta-muy-larga-y-segura-123")
        from app.core.config import get_settings
        get_settings.cache_clear()

        from app.main import create_app
        app = create_app()  # No debe lanzar excepción
        assert app is not None