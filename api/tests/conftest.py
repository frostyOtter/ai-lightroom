import pytest

from app.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Clear the get_settings() lru_cache before every test.

    This is critical for monkeypatch to work correctly. Without clearing
    the cache, get_settings() returns the same cached instance regardless
    of any environment variable overrides applied by monkeypatch.
    """
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
