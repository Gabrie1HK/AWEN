from __future__ import annotations


class TestParcelLifecycle:
    def test_full_lifecycle(self, client, auth_headers):
        payload = {
            "sender": "Lifecycle Test",
            "senderId": "76.123.456-7",
            "senderPhone": "+56 9 1234 5678",
            "recipient": "Test Recipient",
            "recipientId": "12.345.678-9",
            "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test 123",
            "originBranch": "Sucursal Central",
            "destinationBranch": "Sucursal Norte",
            "weight": 5.0,
            "dimensions": "30x20x15 cm",
            "declaredValue": 100000,
            "description": "Full lifecycle test",
        }
        create_resp = client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        assert create_resp.status_code == 200
        parcel_id = create_resp.json()["id"]
        guide = create_resp.json()["guide"]

        get_resp = client.get(f"/api/v1/parcels/{parcel_id}", headers=auth_headers)
        assert get_resp.status_code == 200
        assert get_resp.json()["status"] == "Registered"

        tracking_resp = client.get(f"/api/v1/parcels/{guide}/tracking", headers=auth_headers)
        assert tracking_resp.status_code == 200
        assert len(tracking_resp.json()) >= 1
        assert tracking_resp.json()[0]["step"] == "Registered"

        status_resp = client.post(
            f"/api/v1/parcels/{parcel_id}/status",
            headers=auth_headers,
            json={"status": "Picked Up"},
        )
        assert status_resp.status_code == 200
        assert status_resp.json()["status"] == "Picked Up"

        public_resp = client.get(f"/api/v1/tracking/{guide}")
        assert public_resp.status_code == 200
        assert public_resp.json()["parcel"]["status"] == "Picked Up"

    def test_cancel_after_status_change(self, client, auth_headers):
        client.post(
            "/api/v1/parcels/ENV-007/status",
            headers=auth_headers,
            json={"status": "Picked Up"},
        )
        cancel_resp = client.post("/api/v1/parcels/ENV-007/cancel", headers=auth_headers)
        assert cancel_resp.status_code == 200
        assert cancel_resp.json()["status"] == "Returned"

        get_resp = client.get("/api/v1/parcels/ENV-007", headers=auth_headers)
        assert get_resp.json()["status"] == "Returned"


class TestBatchWorkflow:
    def test_batch_create_assign_and_update(self, client, auth_headers):
        create_resp = client.post(
            "/api/v1/logistics/batches",
            headers=auth_headers,
            json={"parcels": ["ENV-001"]},
        )
        assert create_resp.status_code == 200
        batch_id = create_resp.json()["id"]
        assert create_resp.json()["status"] == "Pending Assignment"

        assign_resp = client.post(
            f"/api/v1/logistics/batches/{batch_id}/assign",
            headers=auth_headers,
            json={"vehicle": "ABC-123", "driver": "Conductor Pedro"},
        )
        assert assign_resp.status_code == 200
        assert assign_resp.json()["status"] == "Assigned"

        update_resp = client.patch(
            f"/api/v1/logistics/batches/{batch_id}",
            headers=auth_headers,
            json={"driver": "Nuevo Conductor"},
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["driver"] == "Nuevo Conductor"

    def test_batch_not_found_after_delete(self, client, auth_headers):
        get_resp = client.get("/api/v1/logistics/batches/LOT-999", headers=auth_headers)
        assert get_resp.status_code == 404


class TestUserProfileWorkflow:
    def test_get_and_update_own_profile(self, client, auth_headers, admin_user):
        me_resp = client.get("/api/v1/users/me", headers=auth_headers)
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == "admin@awen.com"

        update_resp = client.patch(
            "/api/v1/users/me",
            headers=auth_headers,
            json={"phone": "+58 999 888 7777"},
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["phone"] == "+58 999 888 7777"

        me_again = client.get("/api/v1/users/me", headers=auth_headers)
        assert me_again.json()["phone"] == "+58 999 888 7777"
