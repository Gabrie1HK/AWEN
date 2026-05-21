from __future__ import annotations


class TestBranches:
    def test_list_branches(self, client, auth_headers):
        response = client.get("/api/v1/branches", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 6
        assert len(body["data"]) >= 5

    def test_get_branch(self, client, auth_headers):
        response = client.get("/api/v1/branches/1", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Sucursal Central"

    def test_create_branch(self, client, auth_headers):
        response = client.post(
            "/api/v1/branches",
            headers=auth_headers,
            json={
                "name": "Sucursal Test",
                "city": "Test City",
                "address": "Test 123",
                "manager": "Test Manager",
                "phone": "+56 9 0000 0000",
            },
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Sucursal Test"

    def test_create_branch_with_all_fields(self, client, auth_headers):
        response = client.post(
            "/api/v1/branches",
            headers=auth_headers,
            json={
                "name": "Sucursal Nueva",
                "city": "Caracas",
                "address": "Av. Principal 456",
                "manager": "Nuevo Manager",
                "phone": "+58 212 555 5555",
            },
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Sucursal Nueva"

    def test_update_branch(self, client, auth_headers):
        response = client.patch(
            "/api/v1/branches/1",
            headers=auth_headers,
            json={"manager": "Nuevo Manager"},
        )
        assert response.status_code == 200
        assert response.json()["manager"] == "Nuevo Manager"

    def test_get_nonexistent_branch(self, client, auth_headers):
        response = client.get("/api/v1/branches/999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_nonexistent_branch(self, client, auth_headers):
        response = client.patch(
            "/api/v1/branches/999",
            headers=auth_headers,
            json={"name": "Ghost Branch"},
        )
        assert response.status_code == 404

    def test_delete_nonexistent_branch(self, client, auth_headers):
        response = client.delete("/api/v1/branches/999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_branch_soft(self, client, auth_headers):
        response = client.delete("/api/v1/branches/1", headers=auth_headers)
        assert response.status_code == 200
        get_response = client.get("/api/v1/branches/1", headers=auth_headers)
        assert get_response.json()["active"] is False
