from __future__ import annotations


class TestDeliveries:
    def test_list_deliveries(self, client, auth_headers):
        response = client.get("/api/v1/deliveries", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3

    def test_get_delivery(self, client, auth_headers):
        response = client.get("/api/v1/deliveries/DEL-001", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["status"] == "Completed"

    def test_update_delivery(self, client, auth_headers):
        response = client.patch(
            "/api/v1/deliveries/DEL-002",
            headers=auth_headers,
            json={"gps": "-33.0, -71.0"},
        )
        assert response.status_code == 200
        assert response.json()["gps"] == "-33.0, -71.0"

    def test_add_pod(self, client, auth_headers):
        response = client.post(
            "/api/v1/deliveries/DEL-002/pod",
            headers=auth_headers,
            json={
                "podType": "Signature",
                "signatureData": "data:image/png;base64,...",
                "gps": "-33.0, -71.0",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Completed"
        assert data["podType"] == "Signature"
