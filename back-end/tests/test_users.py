from __future__ import annotations


class TestUsers:
    def test_list_users(self, client, auth_headers):
        response = client.get("/api/v1/users", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 7
        assert len(body["data"]) >= 5

    def test_list_users_filter_by_role(self, client, auth_headers):
        response = client.get(
            "/api/v1/users?role=Admin",
            headers=auth_headers,
        )
        assert response.status_code == 200
        body = response.json()
        assert all(u["role"] == "Admin" for u in body["data"])

    def test_get_user(self, client, auth_headers):
        response = client.get("/api/v1/users/1", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Admin Principal"

    def test_create_user(self, client, auth_headers):
        response = client.post(
            "/api/v1/users",
            headers=auth_headers,
            json={
                "name": "Test User",
                "email": "test@awen.com",
                "role": "Warehouse Operator",
                "branch": "Sucursal Central",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test User"
        assert data["active"] is True

    def test_update_user(self, client, auth_headers):
        response = client.patch(
            "/api/v1/users/1",
            headers=auth_headers,
            json={"name": "Admin Renamed"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Admin Renamed"

    def test_get_nonexistent_user(self, client, auth_headers):
        response = client.get("/api/v1/users/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_nonexistent_user(self, client, auth_headers):
        response = client.patch(
            "/api/v1/users/9999",
            headers=auth_headers,
            json={"name": "Ghost"},
        )
        assert response.status_code == 404

    def test_delete_nonexistent_user(self, client, auth_headers):
        response = client.delete("/api/v1/users/9999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_user_soft(self, client, auth_headers):
        response = client.delete("/api/v1/users/1", headers=auth_headers)
        assert response.status_code == 200
        get_response = client.get("/api/v1/users/1", headers=auth_headers)
        assert get_response.json()["active"] is False

    def test_reset_password(self, client, auth_headers):
        response = client.patch(
            "/api/v1/users/1/password",
            headers=auth_headers,
            json={"new_password": "nuevaClave123"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_reset_password_nonexistent_user(self, client, auth_headers):
        response = client.patch(
            "/api/v1/users/9999/password",
            headers=auth_headers,
            json={"new_password": "nuevaClave123"},
        )
        assert response.status_code == 404

    def test_reset_password_short_password(self, client, auth_headers):
        response = client.patch(
            "/api/v1/users/1/password",
            headers=auth_headers,
            json={"new_password": "abc"},
        )
        assert response.status_code == 422

    def test_reset_password_requires_auth(self, client):
        response = client.patch(
            "/api/v1/users/1/password",
            json={"new_password": "nuevaClave123"},
        )
        assert response.status_code == 401
