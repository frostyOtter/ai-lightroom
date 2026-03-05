import os
import pytest
from unittest.mock import patch, MagicMock
from app.config import Settings, get_settings, settings


class TestSettings:
    """Test Settings class initialization and properties."""

    def test_default_values(self):
        """Test that Settings loads with default values."""
        test_settings = Settings()
        assert test_settings.API_HOST == "0.0.0.0"
        assert test_settings.API_PORT == 8000
        assert test_settings.DEBUG is True
        assert test_settings.GOOGLE_MODEL == "gemini-1.5-pro-vision"
        assert test_settings.GOOGLE_MODEL_TEXT == "gemini-1.5-pro"
        assert test_settings.MAX_UPLOAD_SIZE == 10485760
        assert test_settings.LOG_LEVEL == "INFO"
        assert test_settings.LOG_FORMAT == "json"
        assert test_settings.RATE_LIMIT_PER_MINUTE == 60

    def test_cors_origins_property(self):
        """Test CORS origins property parsing."""
        test_settings = Settings(
            CORS_ORIGINS="http://localhost:5173,http://localhost:3000"
        )
        origins = test_settings.cors_origins_list
        assert origins == ["http://localhost:5173", "http://localhost:3000"]

    def test_cors_origins_property_single(self):
        """Test CORS origins with single origin."""
        test_settings = Settings(CORS_ORIGINS="http://localhost:5173")
        origins = test_settings.cors_origins_list
        assert origins == ["http://localhost:5173"]

    def test_cors_origins_property_with_spaces(self):
        """Test CORS origins with whitespace."""
        test_settings = Settings(
            CORS_ORIGINS="http://localhost:5173, http://localhost:3000"
        )
        origins = test_settings.cors_origins_list
        assert origins == ["http://localhost:5173", "http://localhost:3000"]

    def test_allowed_extensions_property(self):
        """Test allowed extensions property parsing."""
        test_settings = Settings(ALLOWED_EXTENSIONS="jpg,jpeg,png,webp")
        extensions = test_settings.allowed_extensions_list
        assert extensions == ["jpg", "jpeg", "png", "webp"]

    def test_allowed_extensions_case_insensitive(self):
        """Test allowed extensions are normalized to lowercase."""
        test_settings = Settings(ALLOWED_EXTENSIONS="JPG,JPEG,PNG")
        extensions = test_settings.allowed_extensions_list
        assert extensions == ["jpg", "jpeg", "png"]

    def test_allowed_extensions_with_spaces(self):
        """Test allowed extensions with whitespace."""
        test_settings = Settings(ALLOWED_EXTENSIONS="jpg, jpeg, png")
        extensions = test_settings.allowed_extensions_list
        assert extensions == ["jpg", "jpeg", "png"]

    def test_config_env_file(self):
        """Test that Config class loads from .env file."""
        test_settings = Settings()
        assert test_settings.Config.env_file == ".env"

    def test_config_case_sensitive(self):
        """Test that Config is case sensitive."""
        test_settings = Settings()
        assert test_settings.Config.case_sensitive is True


class TestSettingsValidation:
    """Test Settings validation methods."""

    def test_validate_required_with_valid_key(self, monkeypatch):
        """Test validation passes with valid API key."""
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-test-key-12345")
        test_settings = Settings()
        should_not_raise = test_settings.validate_required()
        assert should_not_raise is None

    def test_validate_required_missing_api_key(self, monkeypatch):
        """Test validation fails with missing API key."""
        monkeypatch.setenv("GOOGLE_API_KEY", "")
        monkeypatch.setenv("GOOGLE_API_KEY", "")
        test_settings = Settings()

        with pytest.raises(SystemExit) as exc_info:
            test_settings.validate_required()
        assert exc_info.value.code == 1

    def test_validate_required_placeholder_api_key(self, monkeypatch):
        """Test validation fails with placeholder API key."""
        monkeypatch.setenv("GOOGLE_API_KEY", "your_gemini_api_key_here")
        test_settings = Settings()

        with pytest.raises(SystemExit) as exc_info:
            test_settings.validate_required()
        assert exc_info.value.code == 1

    def test_validate_required_invalid_port(self, monkeypatch):
        """Test validation fails with invalid port number."""
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-key")
        monkeypatch.setenv("API_PORT", "70000")
        test_settings = Settings()

        with pytest.raises(SystemExit) as exc_info:
            test_settings.validate_required()
        assert exc_info.value.code == 1

    def test_validate_required_port_zero(self, monkeypatch):
        """Test validation fails with port 0."""
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-key")
        monkeypatch.setenv("API_PORT", "0")
        test_settings = Settings()

        with pytest.raises(SystemExit) as exc_info:
            test_settings.validate_required()
        assert exc_info.value.code == 1

    def test_validate_required_port_negative(self, monkeypatch):
        """Test validation fails with negative port."""
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-key")
        monkeypatch.setenv("API_PORT", "-1")
        test_settings = Settings()

        with pytest.raises(SystemExit) as exc_info:
            test_settings.validate_required()
        assert exc_info.value.code == 1

    def test_validate_required_invalid_upload_size(self, monkeypatch):
        """Test validation fails with invalid upload size."""
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-key")
        monkeypatch.setenv("MAX_UPLOAD_SIZE", "0")
        test_settings = Settings()

        with pytest.raises(SystemExit) as exc_info:
            test_settings.validate_required()
        assert exc_info.value.code == 1

    def test_validate_required_negative_upload_size(self, monkeypatch):
        """Test validation fails with negative upload size."""
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-key")
        monkeypatch.setenv("MAX_UPLOAD_SIZE", "-100")
        test_settings = Settings()

        with pytest.raises(SystemExit) as exc_info:
            test_settings.validate_required()
        assert exc_info.value.code == 1

    def test_validate_required_valid_port_range(self, monkeypatch):
        """Test validation passes with valid port numbers."""
        monkeypatch.setenv("GOOGLE_API_KEY", "valid-key")

        for port in [1, 80, 443, 8000, 65535]:
            monkeypatch.setenv("API_PORT", str(port))
            test_settings = Settings()
            should_not_raise = test_settings.validate_required()
            assert should_not_raise is None


class TestGetSettings:
    """Test get_settings singleton function."""

    @patch("app.config.get_settings.cache_clear")
    def test_get_settings_caches_result(self, mock_cache_clear):
        """Test that get_settings caches the settings instance."""
        result1 = get_settings()
        result2 = get_settings()
        assert result1 is result2

    def test_get_settings_calls_validate(self, monkeypatch):
        """Test that get_settings calls validate_required."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key")
        test_settings = get_settings()
        assert test_settings is not None
        assert test_settings.GOOGLE_API_KEY == "test-key"


class TestSettingsEnvVars:
    """Test Settings loading from environment variables."""

    def test_load_from_env_api_host(self, monkeypatch):
        """Test loading API_HOST from environment."""
        monkeypatch.setenv("API_HOST", "127.0.0.1")
        test_settings = Settings()
        assert test_settings.API_HOST == "127.0.0.1"

    def test_load_from_env_api_port(self, monkeypatch):
        """Test loading API_PORT from environment."""
        monkeypatch.setenv("API_PORT", "9000")
        test_settings = Settings()
        assert test_settings.API_PORT == 9000

    def test_load_from_env_debug(self, monkeypatch):
        """Test loading DEBUG from environment."""
        monkeypatch.setenv("DEBUG", "false")
        test_settings = Settings()
        assert test_settings.DEBUG is False

    def test_load_from_env_google_api_key(self, monkeypatch):
        """Test loading GOOGLE_API_KEY from environment."""
        monkeypatch.setenv("GOOGLE_API_KEY", "test-api-key")
        test_settings = Settings()
        assert test_settings.GOOGLE_API_KEY == "test-api-key"

    def test_load_from_env_google_model(self, monkeypatch):
        """Test loading GOOGLE_MODEL from environment."""
        monkeypatch.setenv("GOOGLE_MODEL", "gemini-2.0-pro")
        test_settings = Settings()
        assert test_settings.GOOGLE_MODEL == "gemini-2.0-pro"

    def test_load_from_env_cors_origins(self, monkeypatch):
        """Test loading CORS_ORIGINS from environment."""
        monkeypatch.setenv("CORS_ORIGINS", "http://example.com,http://test.com")
        test_settings = Settings()
        assert test_settings.cors_origins_list == [
            "http://example.com",
            "http://test.com",
        ]

    def test_load_from_env_max_upload_size(self, monkeypatch):
        """Test loading MAX_UPLOAD_SIZE from environment."""
        monkeypatch.setenv("MAX_UPLOAD_SIZE", "20971520")
        test_settings = Settings()
        assert test_settings.MAX_UPLOAD_SIZE == 20971520

    def test_load_from_env_log_level(self, monkeypatch):
        """Test loading LOG_LEVEL from environment."""
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        test_settings = Settings()
        assert test_settings.LOG_LEVEL == "DEBUG"

    def test_load_from_env_rate_limit(self, monkeypatch):
        """Test loading RATE_LIMIT_PER_MINUTE from environment."""
        monkeypatch.setenv("RATE_LIMIT_PER_MINUTE", "120")
        test_settings = Settings()
        assert test_settings.RATE_LIMIT_PER_MINUTE == 120
