from __future__ import annotations

import pytest


class TestParcelValidation:
    def test_create_parcel_empty_body(self, client, auth_headers):
        response = client.post("/api/v1/parcels", headers=auth_headers, json={})
        assert response.status_code == 422

    def test_create_parcel_missing_sender(self, client, auth_headers):
        payload = {
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
        response = client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        assert response.status_code == 422

    def test_create_parcel_missing_recipient(self, client, auth_headers):
        payload = {
            "sender": "Test",
            "senderId": "76.123.456-7",
            "senderPhone": "+56 9 1234 5678",
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
        response = client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        assert response.status_code == 422

    def test_create_parcel_negative_weight_allowed_by_schema(self, client, auth_headers):
        payload = {
            "sender": "Test",
            "senderId": "76.123.456-7",
            "senderPhone": "+56 9 1234 5678",
            "recipient": "Test",
            "recipientId": "12.345.678-9",
            "recipientPhone": "+56 9 8765 4321",
            "recipientAddress": "Test 123",
            "originBranch": "Central",
            "destinationBranch": "Norte",
            "weight": -1.0,
            "dimensions": "30x20x15 cm",
            "declaredValue": 100000,
            "description": "Test",
        }
        response = client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        assert response.status_code == 200

    def test_update_parcel_invalid_status(self, client, auth_headers):
        response = client.patch(
            "/api/v1/parcels/ENV-001",
            headers=auth_headers,
            json={"status": "InvalidStatus"},
        )
        assert response.status_code == 422

    def test_status_update_invalid_status(self, client, auth_headers):
        response = client.post(
            "/api/v1/parcels/ENV-007/status",
            headers=auth_headers,
            json={"status": "Flying"},
        )
        assert response.status_code == 422

    def test_create_parcel_empty_sender_id_allowed_by_schema(self, client, auth_headers):
        payload = {
            "sender": "Test",
            "senderId": "",
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
        response = client.post("/api/v1/parcels", headers=auth_headers, json=payload)
        assert response.status_code == 200


class TestUserValidation:
    def test_create_user_empty_body(self, client, auth_headers):
        response = client.post("/api/v1/users", headers=auth_headers, json={})
        assert response.status_code == 422

    def test_create_user_missing_name(self, client, auth_headers):
        response = client.post(
            "/api/v1/users",
            headers=auth_headers,
            json={"email": "test@awen.com", "role": "Admin"},
        )
        assert response.status_code == 422

    def test_create_user_email_not_validated_by_schema(self, client, auth_headers):
        response = client.post(
            "/api/v1/users",
            headers=auth_headers,
            json={"name": "Test", "email": "not-an-email", "role": "Admin"},
        )
        assert response.status_code == 200

    def test_create_user_invalid_role(self, client, auth_headers):
        response = client.post(
            "/api/v1/users",
            headers=auth_headers,
            json={"name": "Test", "email": "test@awen.com", "role": "SuperAdmin"},
        )
        assert response.status_code == 422


class TestBranchValidation:
    def test_create_branch_empty_body(self, client, auth_headers):
        response = client.post("/api/v1/branches", headers=auth_headers, json={})
        assert response.status_code == 422

    def test_create_branch_missing_name(self, client, auth_headers):
        response = client.post(
            "/api/v1/branches",
            headers=auth_headers,
            json={"city": "Test", "address": "Test 123"},
        )
        assert response.status_code == 422


class TestBatchValidation:
    def test_create_batch_empty_body_defaults(self, client, auth_headers):
        response = client.post("/api/v1/logistics/batches", headers=auth_headers, json={})
        assert response.status_code == 200
        assert response.json()["status"] == "Pending Assignment"
        assert response.json()["parcelCount"] == 0

    def test_create_batch_invalid_parcels_type(self, client, auth_headers):
        response = client.post(
            "/api/v1/logistics/batches",
            headers=auth_headers,
            json={"parcels": "not-a-list"},
        )
        assert response.status_code == 422

    def test_assign_batch_missing_fields(self, client, auth_headers):
        response = client.post(
            "/api/v1/logistics/batches/LOT-002/assign",
            headers=auth_headers,
            json={},
        )
        assert response.status_code == 422

    def test_assign_batch_empty_vehicle_allowed_by_schema(self, client, auth_headers):
        response = client.post(
            "/api/v1/logistics/batches/LOT-002/assign",
            headers=auth_headers,
            json={"vehicle": "", "driver": "Conductor Pedro"},
        )
        assert response.status_code == 200


class TestDeliveryValidation:
    def test_update_delivery_empty_body(self, client, auth_headers):
        response = client.patch(
            "/api/v1/deliveries/DEL-002",
            headers=auth_headers,
            json={},
        )
        assert response.status_code == 200

    def test_add_pod_empty_body(self, client, auth_headers):
        response = client.post(
            "/api/v1/deliveries/DEL-002/pod",
            headers=auth_headers,
            json={},
        )
        assert response.status_code == 422

    def test_add_pod_missing_pod_type(self, client, auth_headers):
        response = client.post(
            "/api/v1/deliveries/DEL-002/pod",
            headers=auth_headers,
            json={"signatureData": "data:image/png;base64,..."},
        )
        assert response.status_code == 422


class TestPaginationValidation:
    def test_parcels_negative_page(self, client, auth_headers):
        response = client.get("/api/v1/parcels?page=-1", headers=auth_headers)
        assert response.status_code == 422

    def test_parcels_zero_page_size(self, client, auth_headers):
        response = client.get("/api/v1/parcels?pageSize=0", headers=auth_headers)
        assert response.status_code == 422

    def test_parcels_excessive_page_size(self, client, auth_headers):
        response = client.get("/api/v1/parcels?pageSize=999", headers=auth_headers)
        assert response.status_code == 422

    def test_parcels_page_exceeds_total(self, client, auth_headers):
        response = client.get("/api/v1/parcels?page=9999", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) == 0
        assert body["total"] >= 7

    def test_invalid_status_filter(self, client, auth_headers):
        response = client.get("/api/v1/parcels?status=NonExistent", headers=auth_headers)
        assert response.status_code == 422

    def test_empty_status_filter(self, client, auth_headers):
        response = client.get("/api/v1/parcels?status=Out for Delivery", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert len(body["data"]) == 0
