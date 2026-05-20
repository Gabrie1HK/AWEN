from __future__ import annotations


class TestParcelList:
    def test_list_parcels_requires_auth(self, client):
        response = client.get("/api/v1/parcels")
        assert response.status_code == 401

    def test_list_parcels(self, client, auth_headers):
        response = client.get("/api/v1/parcels", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["total"] >= 7
        assert body["data"][0]["guide"] == "AWEN-2026-0001"

    def test_list_parcels_filter_by_status(self, client, auth_headers):
        response = client.get(
            "/api/v1/parcels?status=Delivered",
            headers=auth_headers,
        )
        assert response.status_code == 200
        body = response.json()
        assert all(p["status"] == "Delivered" for p in body["data"])
        assert len(body["data"]) == 1

    def test_list_parcels_search(self, client, auth_headers):
        response = client.get(
            "/api/v1/parcels?search=TechStore",
            headers=auth_headers,
        )
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) >= 1
        assert "TechStore" in body["data"][0]["sender"]

    def test_list_parcels_pagination(self, client, auth_headers):
        response = client.get(
            "/api/v1/parcels?page=1&pageSize=2",
            headers=auth_headers,
        )
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) == 2
        assert body["page"] == 1
        assert body["pageSize"] == 2
        assert body["total"] >= 7


class TestParcelCRUD:
    def test_get_parcel(self, client, auth_headers):
        response = client.get("/api/v1/parcels/ENV-001", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["guide"] == "AWEN-2026-0001"

    def test_get_parcel_not_found(self, client, auth_headers):
        response = client.get("/api/v1/parcels/ENV-999", headers=auth_headers)
        assert response.status_code == 404

    def test_create_parcel(self, client, auth_headers):
        payload = {
            "sender": "Test Sender",
            "senderId": "76.123.456-7",
            "senderPhone": "+56 9 1234 5678",
            "recipient": "Test Recipient",
            "recipientId": "12.345.678-9",
            "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test Address 123",
            "originBranch": "Sucursal Central",
            "destinationBranch": "Sucursal Norte",
            "weight": 5.0,
            "dimensions": "30x20x15 cm",
            "declaredValue": 100000,
            "description": "Test package",
        }
        response = client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["sender"] == "Test Sender"
        assert data["status"] == "Registered"
        assert data["guide"].startswith("AWEN-2026-")

    def test_update_parcel(self, client, auth_headers):
        response = client.patch(
            "/api/v1/parcels/ENV-001",
            headers=auth_headers,
            json={"description": "Updated description"},
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Updated description"


class TestParcelStatus:
    def test_update_status_valid(self, client, auth_headers):
        response = client.post(
            "/api/v1/parcels/ENV-007/status",
            headers=auth_headers,
            json={"status": "Picked Up"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "Picked Up"

    def test_update_status_skip_not_allowed(self, client, auth_headers):
        response = client.post(
            "/api/v1/parcels/ENV-007/status",
            headers=auth_headers,
            json={"status": "Delivered"},
        )
        assert response.status_code == 422
        assert "no se puede saltar" in response.json()["detail"]["message"].lower()

    def test_update_status_rollback_not_allowed(self, client, auth_headers):
        response = client.post(
            "/api/v1/parcels/ENV-001/status",
            headers=auth_headers,
            json={"status": "Registered"},
        )
        assert response.status_code == 422
        assert "retroceder" in response.json()["detail"]["message"].lower()

    def test_update_status_from_delivered_blocked(self, client, auth_headers):
        response = client.post(
            "/api/v1/parcels/ENV-002/status",
            headers=auth_headers,
            json={"status": "Returned"},
        )
        assert response.status_code == 422

    def test_cancel_parcel(self, client, auth_headers):
        response = client.post(
            "/api/v1/parcels/ENV-003/cancel",
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "Returned"

    def test_tracking_history(self, client, auth_headers):
        response = client.get(
            "/api/v1/parcels/AWEN-2026-0001/tracking",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 6
        assert data[0]["step"] == "Registered"
        assert data[0]["completed"] is True


class TestPublicTracking:
    def test_public_tracking_found(self, client):
        response = client.get("/api/v1/tracking/AWEN-2026-0001")
        assert response.status_code == 200
        data = response.json()
        assert data["guide"] == "AWEN-2026-0001"
        assert data["parcel"] is not None
        assert len(data["history"]) >= 1

    def test_public_tracking_not_found(self, client):
        response = client.get("/api/v1/tracking/INVALID-GUIDE")
        assert response.status_code == 200
        data = response.json()
        assert data["parcel"] is None
        assert data["history"] is None
