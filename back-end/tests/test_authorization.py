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


class TestMultiRoleAccess:
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

    def test_all_roles_can_create_parcel(self, client, auth_headers, operator_headers, driver_headers, client_headers):
        payload = {
            "sender": "Multi Role Test",
            "senderId": "76.123.456-7",
            "senderPhone": "+56 9 1234 5678",
            "recipient": "Test",
            "recipientId": "12.345.678-9",
            "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test 123",
            "originBranch": "Central",
            "destinationBranch": "Norte",
            "weight": 5.0,
            "dimensions": "30x20x15 cm",
            "declaredValue": 100000,
            "description": "Test",
        }
        for role, headers in [("Admin", auth_headers), ("Operator", operator_headers),
                              ("Driver", driver_headers), ("Client", client_headers)]:
            response = client.post("/api/v1/parcels", headers=headers, json=payload)
            assert response.status_code == 200, f"{role} failed to create parcel"

    def test_all_roles_can_list_users(self, client, auth_headers, operator_headers, driver_headers, client_headers):
        for role, headers in [("Admin", auth_headers), ("Operator", operator_headers),
                              ("Driver", driver_headers), ("Client", client_headers)]:
            response = client.get("/api/v1/users", headers=headers)
            assert response.status_code == 200, f"{role} failed to list users"

    def test_all_roles_can_view_dashboard(self, client, auth_headers, operator_headers, driver_headers, client_headers):
        for role, headers in [("Admin", auth_headers), ("Operator", operator_headers),
                              ("Driver", driver_headers), ("Client", client_headers)]:
            response = client.get("/api/v1/dashboard", headers=headers)
            assert response.status_code == 200, f"{role} failed to view dashboard"

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
