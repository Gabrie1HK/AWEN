from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure app is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from app.main import create_app
from app.repositories.parcels import InMemoryParcelRepository, InMemoryTrackingRepository
from app.repositories.users import InMemoryUserRepository
from app.services.parcels import ParcelService
from app.services.auth import AuthService
from app.services.seed import seed_users
from app.services.seed_parcels import seed_parcels, seed_tracking_history


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user_repo():
    return InMemoryUserRepository(seed_users())


@pytest.fixture
def auth_service(user_repo):
    return AuthService(user_repo)


@pytest.fixture
def parcel_repo():
    return InMemoryParcelRepository(seed_parcels())


@pytest.fixture
def tracking_repo():
    return InMemoryTrackingRepository(seed_tracking_history())


@pytest.fixture
def parcel_service(parcel_repo, tracking_repo):
    return ParcelService(parcel_repo, tracking_repo)


@pytest.fixture
def auth_token(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@awen.cl", "password": "123456"},
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
