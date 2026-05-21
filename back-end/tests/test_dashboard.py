from __future__ import annotations


class TestDashboard:
    def test_dashboard(self, client, auth_headers):
        response = client.get("/api/v1/dashboard", headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert "kpis" in body
        assert "dailyShipments" in body
        assert "deliveriesByBranch" in body
        assert "recentActivity" in body

    def test_kpis_in_dashboard(self, client, auth_headers):
        response = client.get("/api/v1/dashboard", headers=auth_headers)
        body = response.json()
        kpis = body["kpis"]
        assert "totalShipments" in kpis
        assert "inTransit" in kpis
        assert "delivered" in kpis
        assert "returned" in kpis

    def test_dashboard_requires_auth(self, client):
        response = client.get("/api/v1/dashboard")
        assert response.status_code == 401

    def test_dashboard_empty_data(self, empty_data_client, empty_data_headers):
        response = empty_data_client.get("/api/v1/dashboard", headers=empty_data_headers)
        assert response.status_code == 200
        body = response.json()
        assert "kpis" in body
        assert "dailyShipments" in body
        assert "deliveriesByBranch" in body
        assert "recentActivity" in body
