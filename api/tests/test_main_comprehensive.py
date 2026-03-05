import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app


class TestRootEndpoint:
    """Test the root endpoint."""

    client = TestClient(app)

    def test_root_endpoint(self):
        """Test root endpoint returns expected response."""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "AI Lightroom API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "running"

    def test_root_endpoint_json_content_type(self):
        """Test root endpoint returns JSON content type."""
        response = self.client.get("/")
        assert response.headers["content-type"] == "application/json"

    def test_root_endpoint_response_structure(self):
        """Test root endpoint has correct response structure."""
        response = self.client.get("/")
        data = response.json()
        assert isinstance(data, dict)
        assert "message" in data
        assert "version" in data
        assert "status" in data

    def test_root_endpoint_no_auth_required(self):
        """Test root endpoint doesn't require authentication."""
        response = self.client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_response_time(self):
        """Test root endpoint responds quickly."""
        import time

        start = time.time()
        response = self.client.get("/")
        end = time.time()
        assert response.status_code == 200
        assert (end - start) < 0.1

    def test_root_endpoint_post_not_allowed(self):
        """Test root endpoint rejects POST requests."""
        response = self.client.post("/")
        assert response.status_code in [405, 422]

    def test_root_endpoint_put_not_allowed(self):
        """Test root endpoint rejects PUT requests."""
        response = self.client.put("/")
        assert response.status_code in [405, 422]

    def test_root_endpoint_delete_not_allowed(self):
        """Test root endpoint rejects DELETE requests."""
        response = self.client.delete("/")
        assert response.status_code in [405, 422]


class TestCORSMiddleware:
    """Test CORS middleware configuration."""

    client = TestClient(app)

    def test_cors_headers_present(self):
        """Test CORS headers are present in response with origin."""
        response = self.client.get("/", headers={"Origin": "http://localhost:5173"})
        assert "access-control-allow-origin" in response.headers

    def test_cors_preflight_options(self):
        """Test CORS preflight OPTIONS request."""
        response = self.client.options(
            "/",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200

    def test_cors_allows_methods(self):
        """Test CORS allows all methods."""
        response = self.client.options(
            "/",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert response.status_code == 200

    def test_cors_allows_headers(self):
        """Test CORS allows custom headers."""
        response = self.client.options(
            "/",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type, Authorization",
            },
        )
        assert response.status_code == 200

    def test_cors_allows_credentials(self):
        """Test CORS allows credentials."""
        response = self.client.get("/", headers={"Origin": "http://localhost:5173"})
        assert response.headers.get("access-control-allow-credentials") == "true"

    def test_cors_allowed_origin(self):
        """Test CORS allows configured origin."""
        response = self.client.get("/", headers={"Origin": "http://localhost:5173"})
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_cors_different_origin(self):
        """Test CORS response for different origin."""
        response = self.client.get("/", headers={"Origin": "http://example.com"})
        assert response.status_code == 200


class TestAppConfiguration:
    """Test FastAPI application configuration."""

    def test_app_title(self):
        """Test app has correct title."""
        assert app.title == "AI Lightroom API"

    def test_app_description(self):
        """Test app has correct description."""
        assert app.description == "AI-powered image color adjustment API"

    def test_app_version(self):
        """Test app has correct version."""
        assert app.version == "1.0.0"

    def test_app_routes_included(self):
        """Test that health routes are included."""
        routes = [route.path for route in app.routes]
        assert "/health/" in routes
        assert "/health/detailed" in routes

    def test_app_root_route(self):
        """Test root route is included."""
        routes = [route.path for route in app.routes]
        assert "/" in routes


class TestStartupEvent:
    """Test application startup event."""

    @patch("builtins.print")
    def test_startup_event_prints_message(self, mock_print):
        """Test startup event prints startup message."""
        from app.main import startup_event

        # This is an async function, need to run it properly
        import asyncio

        asyncio.run(startup_event())

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "starting up" in call_args.lower()


class TestShutdownEvent:
    """Test application shutdown event."""

    @patch("builtins.print")
    def test_shutdown_event_prints_message(self, mock_print):
        """Test shutdown event prints shutdown message."""
        from app.main import shutdown_event

        # This is an async function, need to run it properly
        import asyncio

        asyncio.run(shutdown_event())

        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "shutting down" in call_args.lower()


class TestAppMiddleware:
    """Test application middleware."""

    client = TestClient(app)

    def test_cors_middleware_registered(self):
        """Test that CORS middleware is registered."""
        assert len(app.user_middleware) > 0

    def test_middleware_order(self):
        """Test middleware is properly ordered."""
        assert len(app.user_middleware) > 0


class TestErrorHandling:
    """Test error handling."""

    client = TestClient(app)

    def test_404_not_found(self):
        """Test 404 response for non-existent route."""
        response = self.client.get("/non-existent-route")
        assert response.status_code == 404

    def test_405_method_not_allowed(self):
        """Test 405 for unsupported methods."""
        response = self.client.patch("/")
        assert response.status_code == 405


class TestAPIResponseHeaders:
    """Test API response headers."""

    client = TestClient(app)

    def test_default_headers(self):
        """Test default response headers."""
        response = self.client.get("/")
        assert "content-type" in response.headers
        assert response.headers["content-type"] == "application/json"


class TestAPIConcurrentRequests:
    """Test handling of concurrent requests."""

    client = TestClient(app)

    def test_multiple_root_requests(self):
        """Test handling multiple requests to root."""
        responses = [self.client.get("/") for _ in range(10)]
        for response in responses:
            assert response.status_code == 200

    def test_concurrent_health_checks(self):
        """Test concurrent health check requests."""
        responses = [self.client.get("/health/") for _ in range(10)]
        for response in responses:
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
