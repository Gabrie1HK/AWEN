from __future__ import annotations


class TestBatches:
    def test_list_batches(self, client, auth_headers):
        response = client.get("/api/v1/logistics/batches", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 4
        assert data[0]["id"] == "LOT-001"

    def test_get_batch(self, client, auth_headers):
        response = client.get("/api/v1/logistics/batches/LOT-001", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "Assigned"

    def test_get_batch_not_found(self, client, auth_headers):
        response = client.get("/api/v1/logistics/batches/LOT-999", headers=auth_headers)
        assert response.status_code == 404

    def test_create_batch(self, client, auth_headers):
        response = client.post(
            "/api/v1/logistics/batches",
            headers=auth_headers,
            json={"parcels": ["ENV-001"]},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "Pending Assignment"

    def test_assign_batch(self, client, auth_headers):
        response = client.post(
            "/api/v1/logistics/batches/LOT-002/assign",
            headers=auth_headers,
            json={"vehicle": "ABC-123", "driver": "Conductor Pedro"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "Assigned"
        assert response.json()["vehicle"] == "ABC-123"


class TestVehicles:
    def test_list_vehicles(self, client, auth_headers):
        response = client.get("/api/v1/logistics/vehicles", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
        assert data[0]["plate"] == "ABC-123"
