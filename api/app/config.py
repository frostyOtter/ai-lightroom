import os
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import sys


class Settings(BaseSettings):
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL: str = "gemini-1.5-pro-vision"
    GOOGLE_MODEL_TEXT: str = "gemini-1.5-pro"

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    MAX_UPLOAD_SIZE: int = 10485760
    ALLOWED_EXTENSIONS: str = "jpg,jpeg,png,webp"

    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    RATE_LIMIT_PER_MINUTE: int = 60

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(",")]

    def validate_required(self) -> None:
        errors = []

        if not self.GOOGLE_API_KEY or self.GOOGLE_API_KEY == "your_gemini_api_key_here":
            errors.append(
                "GOOGLE_API_KEY is required. Get your key from https://makersuite.google.com/app/apikey"
            )

        if self.API_PORT < 1 or self.API_PORT > 65535:
            errors.append(f"Invalid API_PORT: {self.API_PORT}")

        if self.MAX_UPLOAD_SIZE < 1:
            errors.append("MAX_UPLOAD_SIZE must be positive")

        if errors:
            print("\n❌ Configuration Errors:\n")
            for error in errors:
                print(f"  • {error}")
            print("\nPlease check your .env file and try again.\n")
            sys.exit(1)

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_required()
    return settings


# Only instantiate settings if not running tests
if os.environ.get("PYTEST_CURRENT_TEST") is None:
    settings = get_settings()
else:
    # In tests, settings will be accessed through get_settings() function
    settings = None
