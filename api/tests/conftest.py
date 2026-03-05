import os
import pytest


# Set test environment variables before any test runs
os.environ["GOOGLE_API_KEY"] = "test-api-key-for-testing-12345"
os.environ["DEBUG"] = "true"


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Clear settings cache before each test to ensure fresh environment."""
    from app.config import get_settings

    get_settings.cache_clear()
    yield
