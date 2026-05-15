from __future__ import annotations


class TestBranches:
    def test_list_branches(self, client, auth_headers):
        response = client.get("/api/v1/branches", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 6

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

    def test_update_branch(self, client, auth_headers):
        response = client.patch(
            "/api/v1/branches/1",
            headers=auth_headers,
            json={"manager": "Nuevo Manager"},
        )
        assert response.status_code == 200
        assert response.json()["manager"] == "Nuevo Manager"

    def test_delete_branch_soft(self, client, auth_headers):
        response = client.delete("/api/v1/branches/1", headers=auth_headers)
        assert response.status_code == 200
        get_response = client.get("/api/v1/branches/1", headers=auth_headers)
        assert get_response.json()["active"] is False
