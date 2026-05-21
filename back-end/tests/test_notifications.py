from __future__ import annotations


class TestNotifications:
    def test_list_notifications(self, client, auth_headers):
        response = client.get("/api/v1/notifications", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert "data" in body
        assert "total" in body

    def test_list_notifications_has_structure(self, client, auth_headers):
        response = client.get("/api/v1/notifications", headers=auth_headers)
        body = response.json()
        assert "data" in body
        assert "total" in body
        assert body["total"] >= 0

    def test_mark_read(self, client, auth_headers):
        response = client.patch("/api/v1/notifications/nonexistent/read", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_mark_all_read(self, client, auth_headers):
        response = client.patch("/api/v1/notifications/read-all", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    def test_list_requires_auth(self, client):
        response = client.get("/api/v1/notifications")
        assert response.status_code == 401

    def test_notification_created_on_parcel_create(self, client, auth_headers):
        payload = {
            "sender": "Notif Test",
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
            "description": "Notif trigger",
        }
        client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        response = client.get("/api/v1/notifications", headers=auth_headers)
        notifs = response.json()["data"]
        created = [n for n in notifs if n["action_type"] == "parcel_created"]
        assert len(created) >= 1
        assert "Notif Test" in created[0]["text"]

    def test_notification_created_on_status_change(self, client, auth_headers):
        client.post("/api/v1/parcels/ENV-007/status", headers=auth_headers, json={"status": "Picked Up"})
        response = client.get("/api/v1/notifications", headers=auth_headers)
        notifs = response.json()["data"]
        status_notifs = [n for n in notifs if n["action_type"] == "parcel_status"]
        assert len(status_notifs) >= 1

    def test_notification_created_on_cancel(self, client, auth_headers):
        client.post("/api/v1/parcels/ENV-003/cancel", headers=auth_headers)
        response = client.get("/api/v1/notifications", headers=auth_headers)
        notifs = response.json()["data"]
        cancelled = [n for n in notifs if n["action_type"] == "parcel_cancelled"]
        assert len(cancelled) >= 1

    def test_notification_created_on_pod(self, client, auth_headers):
        client.post(
            "/api/v1/deliveries/DEL-002/pod",
            headers=auth_headers,
            json={"podType": "Signature", "signatureData": "data:image/png;base64,...", "gps": "-33.0, -71.0"},
        )
        response = client.get("/api/v1/notifications", headers=auth_headers)
        notifs = response.json()["data"]
        delivery_notifs = [n for n in notifs if n["action_type"] == "delivery_completed"]
        assert len(delivery_notifs) >= 1
