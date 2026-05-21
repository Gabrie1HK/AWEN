from __future__ import annotations


class TestReports:
    def test_kpis(self, client, auth_headers):
        response = client.get("/api/v1/reports/kpis", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["totalShipments"] >= 0
        assert "inTransit" in body
        assert "delivered" in body
        assert "returned" in body

    def test_kpis_with_dates(self, client, auth_headers):
        response = client.get("/api/v1/reports/kpis?dateFrom=2026-05-01&dateTo=2026-05-31", headers=auth_headers)
        assert response.status_code == 200

    def test_daily_volume(self, client, auth_headers):
        response = client.get("/api/v1/reports/daily-volume", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert len(body) > 0
        assert "day" in body[0]
        assert "count" in body[0]

    def test_deliveries_by_branch(self, client, auth_headers):
        response = client.get("/api/v1/reports/deliveries-by-branch", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert len(body) > 0
        assert "branch" in body[0]
        assert "count" in body[0]

    def test_activity(self, client, auth_headers):
        response = client.get("/api/v1/reports/activity", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert len(body) > 0
        assert "time" in body[0]
        assert "action" in body[0]
        assert "user" in body[0]

    def test_summary(self, client, auth_headers):
        response = client.get("/api/v1/reports/summary", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert "totalVolume" in body
        assert "avgDeliveryTime" in body
        assert "successRate" in body

    def test_top_routes(self, client, auth_headers):
        response = client.get("/api/v1/reports/top-routes", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert len(body) > 0
        assert "route" in body[0]
        assert "volume" in body[0]
        assert "avgTime" in body[0]

    def test_export_csv(self, client, auth_headers):
        response = client.get("/api/v1/reports/export?format=csv", headers=auth_headers)
        assert response.status_code == 200
        assert "text/csv" in response.headers.get("content-type", "")
        assert "route" in response.text

    def test_export_unsupported_format(self, client, auth_headers):
        response = client.get("/api/v1/reports/export?format=json", headers=auth_headers)
        assert response.status_code == 400

    def test_kpis_requires_auth(self, client):
        response = client.get("/api/v1/reports/kpis")
        assert response.status_code == 401

    def test_reports_empty_data(self, empty_data_client, empty_data_headers):
        response = empty_data_client.get("/api/v1/reports/kpis", headers=empty_data_headers)
        assert response.status_code == 200
        body = response.json()
        assert "totalShipments" in body
        assert "inTransit" in body
        assert "delivered" in body
        assert "returned" in body

    def test_daily_volume_empty(self, empty_data_client, empty_data_headers):
        response = empty_data_client.get("/api/v1/reports/daily-volume", headers=empty_data_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_deliveries_by_branch_empty(self, empty_data_client, empty_data_headers):
        response = empty_data_client.get("/api/v1/reports/deliveries-by-branch", headers=empty_data_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_activity_empty(self, empty_data_client, empty_data_headers):
        response = empty_data_client.get("/api/v1/reports/activity", headers=empty_data_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
