import pytest
from fastapi.testclient import TestClient
from app.main import app


class TestHealthEndpoints:
    """Test health check endpoints."""

    client = TestClient(app)

    def test_health_check_root(self):
        """Test root health endpoint returns healthy status."""
        response = self.client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert data["service"] == "ai-lightroom-api"

    def test_health_check_detailed(self):
        """Test detailed health endpoint returns component status."""
        response = self.client.get("/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert data["service"] == "ai-lightroom-api"
        assert "components" in data
        assert "database" in data["components"]
        assert "gemini_api" in data["components"]

    def test_health_check_response_structure(self):
        """Test health endpoint response structure."""
        response = self.client.get("/health/")
        data = response.json()
        assert isinstance(data, dict)
        assert "status" in data
        assert "version" in data
        assert "service" in data

    def test_health_detailed_response_structure(self):
        """Test detailed health endpoint response structure."""
        response = self.client.get("/health/detailed")
        data = response.json()
        assert isinstance(data, dict)
        assert "status" in data
        assert "version" in data
        assert "service" in data
        assert "components" in data
        assert isinstance(data["components"], dict)

    def test_health_check_json_content_type(self):
        """Test health endpoint returns JSON content type."""
        response = self.client.get("/health/")
        assert response.headers["content-type"] == "application/json"

    def test_health_detailed_json_content_type(self):
        """Test detailed health endpoint returns JSON content type."""
        response = self.client.get("/health/detailed")
        assert response.headers["content-type"] == "application/json"

    def test_health_check_no_auth_required(self):
        """Test health endpoint doesn't require authentication."""
        response = self.client.get("/health/")
        assert response.status_code == 200

    def test_health_detailed_no_auth_required(self):
        """Test detailed health endpoint doesn't require authentication."""
        response = self.client.get("/health/detailed")
        assert response.status_code == 200

    def test_health_check_response_time(self):
        """Test health endpoint responds quickly."""
        import time

        start = time.time()
        response = self.client.get("/health/")
        end = time.time()
        assert response.status_code == 200
        assert (end - start) < 0.1  # Should respond in < 100ms

    def test_health_detailed_response_time(self):
        """Test detailed health endpoint responds quickly."""
        import time

        start = time.time()
        response = self.client.get("/health/detailed")
        end = time.time()
        assert response.status_code == 200
        assert (end - start) < 0.1  # Should respond in < 100ms

    def test_health_check_status_values(self):
        """Test health status has expected values."""
        response = self.client.get("/health/")
        data = response.json()
        assert data["status"] in ["healthy", "unhealthy"]
        assert isinstance(data["version"], str)
        assert isinstance(data["service"], str)

    def test_health_detailed_component_values(self):
        """Test detailed health components have expected structure."""
        response = self.client.get("/health/detailed")
        data = response.json()
        components = data["components"]
        assert "database" in components
        assert "gemini_api" in components
        assert isinstance(components["database"], str)
        assert isinstance(components["gemini_api"], str)

    def test_health_check_method_not_allowed(self):
        """Test health endpoint rejects POST requests."""
        response = self.client.post("/health/")
        assert response.status_code in [405, 422]

    def test_health_detailed_method_not_allowed(self):
        """Test detailed health endpoint rejects POST requests."""
        response = self.client.post("/health/detailed")
        assert response.status_code in [405, 422]

    def test_health_check_put_not_allowed(self):
        """Test health endpoint rejects PUT requests."""
        response = self.client.put("/health/")
        assert response.status_code in [405, 422]

    def test_health_check_delete_not_allowed(self):
        """Test health endpoint rejects DELETE requests."""
        response = self.client.delete("/health/")
        assert response.status_code in [405, 422]

    def test_health_invalid_path(self):
        """Test invalid health path returns 404."""
        response = self.client.get("/health/invalid")
        assert response.status_code == 404
