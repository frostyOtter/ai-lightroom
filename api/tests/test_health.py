import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    with TestClient(app) as c:
        yield c


class TestRootEndpoint:
    def test_root_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_message(self, client):
        data = client.get("/").json()
        assert data["message"] == "AI Lightroom API"

    def test_root_version(self, client):
        data = client.get("/").json()
        assert data["version"] == "1.0.0"

    def test_root_status(self, client):
        data = client.get("/").json()
        assert data["status"] == "running"


class TestHealthEndpoints:
    def test_health_returns_200(self, client):
        response = client.get("/health/")
        assert response.status_code == 200

    def test_health_status_healthy(self, client):
        data = client.get("/health/").json()
        assert data["status"] == "healthy"

    def test_health_version(self, client):
        data = client.get("/health/").json()
        assert data["version"] == "1.0.0"

    def test_health_service_name(self, client):
        data = client.get("/health/").json()
        assert data["service"] == "ai-lightroom-api"

    def test_health_response_is_json(self, client):
        response = client.get("/health/")
        assert response.headers["content-type"] == "application/json"


class TestDetailedHealthEndpoints:
    def test_detailed_health_returns_200(self, client):
        response = client.get("/health/detailed")
        assert response.status_code == 200

    def test_detailed_health_status_healthy(self, client):
        data = client.get("/health/detailed").json()
        assert data["status"] == "healthy"

    def test_detailed_health_version(self, client):
        data = client.get("/health/detailed").json()
        assert data["version"] == "1.0.0"

    def test_detailed_health_service_name(self, client):
        data = client.get("/health/detailed").json()
        assert data["service"] == "ai-lightroom-api"

    def test_detailed_health_has_components(self, client):
        data = client.get("/health/detailed").json()
        assert "components" in data

    def test_detailed_health_components_has_database(self, client):
        data = client.get("/health/detailed").json()
        assert "database" in data["components"]

    def test_detailed_health_components_has_gemini_api(self, client):
        data = client.get("/health/detailed").json()
        assert "gemini_api" in data["components"]
