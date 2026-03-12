# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Lightroom is a full-stack web application that generates professional-grade color presets for images using AI. Users upload an image, describe their desired style in natural language, and receive AI-generated Lightroom-compatible preset adjustments.

**Technology Stack:**
- **Backend**: FastAPI (Python 3.11+) with Google Gemini AI for image/text processing
- **Frontend**: React 18 with Vite, Tailwind CSS, and Lucide icons
- **Image Processing**: OpenCV (headless), Pillow, NumPy
- **Containerization**: Docker with docker-compose for development

> **Project status**: Infrastructure (Sprint 0) is complete. Core features are not yet implemented — `services/` and `schemas/` directories are intentionally empty placeholders.

## Development Commands

### Docker (Recommended)
```bash
# First time setup - copy environment files
cp .env.example .env
cp api/.env.example api/.env
cp web/.env.example web/.env

# Edit api/.env and add your GOOGLE_API_KEY from https://makersuite.google.com/app/apikey

# Start all services (backend on :8000, frontend on :5173)
docker-compose up

# Rebuild containers (after dependency changes)
docker-compose up --build
```

### Backend (Manual)
```bash
cd api

# Setup (first time only)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --port 8000

# Testing (coverage is auto-enabled via pyproject.toml addopts)
pytest                                                           # All tests
pytest tests/test_health.py                                      # Single file
pytest tests/test_health.py::TestHealthEndpoints::test_health    # Single test
pytest -k "test_name"                                            # By pattern

# Code quality
black .        # Format (line length 88)
ruff check .   # Lint
mypy .         # Type check
```

### Frontend (Manual)
```bash
cd web

# Setup (first time only)
npm install

# Development
npm run dev     # Dev server on :5173
npm run build   # Production build

# Testing & Quality
npm run test    # Vitest (watch mode)
npm run lint    # ESLint (zero-warning policy: --max-warnings 0)
```

## Architecture

### How the Pieces Connect

```
Frontend (React, :5173)
    ↓ axios (VITE_API_URL)
Backend (FastAPI, :8000)
    ├── CORS Middleware (allows :5173, :3000)
    ├── GET /             → service info
    ├── GET /health/      → {"status":"healthy","version":"1.0.0","service":"ai-lightroom-api"}
    └── GET /health/detailed → includes component status (database/gemini_api)
```

In Docker, the `frontend` service waits for the backend health check to pass before starting (`depends_on: backend: condition: service_healthy`). The backend Dockerfiles use volume mounts (`./api:/app`) instead of `COPY . .` — the image alone won't run without docker-compose, but this enables hot reload.

### Backend Key Patterns

- **Settings singleton**: `get_settings()` in `config.py` uses `@lru_cache()`. In tests, `conftest.py` has an `autouse` fixture that clears this cache before every test — critical for `monkeypatch` to work correctly.
- **`settings = None` at module level during tests**: `config.py` sets `settings = None` when `PYTEST_CURRENT_TEST` is in the environment. All route/service code must call `get_settings()` rather than importing the module-level `settings` variable.
- **Router registration**: Each route file creates its own `APIRouter()` and is registered in `main.py` with `app.include_router(router, prefix="...", tags=[...])`.
- **Two Gemini models**: `GOOGLE_MODEL` (default: `gemini-1.5-pro-vision`) for image tasks, `GOOGLE_MODEL_TEXT` (default: `gemini-1.5-pro`) for text-only tasks.
- **`tenacity`** is included for Gemini API retry logic; **`aiofiles`** for async image file I/O; **`python-multipart`** for FastAPI file upload support — all in `requirements.txt` but not yet wired up.

### Frontend Key Patterns

- **API client**: Single axios instance in `src/services/api.js`, configured from `VITE_API_URL` and `VITE_API_TIMEOUT`.
- **Config validation**: `src/config.js` exports a `validateConfig()` function that throws `Error('Invalid configuration')` if required env vars are missing (mirrors backend's startup validation pattern).
- **Feature flags**: `VITE_ENABLE_BATCH_PROCESSING` and `VITE_ENABLE_USER_ACCOUNTS` exist in `config.js` (both default `false`, commented out in `.env.example`).
- **Custom Tailwind color**: `primary` palette (sky blue) is defined — use `text-primary-600`, `bg-primary-500`, etc.
- **Test files**: Co-located with source (e.g., `App.test.jsx` next to `App.jsx`), not in a separate directory.
- **Test globals**: Vitest is configured with `globals: true` so `describe/it/expect` are available without imports.

## Configuration

**Backend (`api/app/config.py`):**
- `GOOGLE_API_KEY` — required; backend exits on startup if missing
- `GOOGLE_MODEL` / `GOOGLE_MODEL_TEXT` — vision vs. text model selection
- `MAX_UPLOAD_SIZE` — default 10MB
- `CORS_ORIGINS` — comma-separated list, split by `cors_origins_list` property

**Frontend (`web/.env`):**
- `VITE_API_URL` — backend endpoint (default: `http://localhost:8000`)
- `VITE_API_TIMEOUT` — ms (default: 30000)
- `VITE_MAX_FILE_SIZE` — must match backend (default: 10485760)

**Test environment**: `GOOGLE_API_KEY=test-api-key-for-testing-12345` and `DEBUG=true` are injected automatically via `pyproject.toml` `[tool.pytest.ini_options]` — do not set them manually.

## Code Style & Conventions

### Python
- **Formatting**: Black (line length 88, target Python 3.11)
- **Linting**: Ruff (rules E, W, F, I, B, C4, UP; `E501` and `B008` ignored)
- **Type hints**: Required everywhere; mypy strict (`disallow_untyped_defs`); `cv2` and `PIL` have `ignore_missing_imports`
- **Naming**: `snake_case` files/functions/vars, `PascalCase` classes, `UPPER_SNAKE_CASE` constants, `_leading_underscore` private methods
- **Imports**: stdlib → third-party → local
- **Docstrings**: Google style (Args/Returns/Raises)
- **Errors**: `HTTPException` for all API errors; 400 for client errors, 500 for unexpected; log before re-raising 500s

### JavaScript/React
- **Components**: Functional with hooks only; `PascalCase.jsx` filenames
- **Naming**: `camelCase` variables/functions, `UPPER_SNAKE_CASE` constants
- **Imports**: node_modules → internal modules (blank line separator)

### Git
Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
Branch naming: `feature/`, `bugfix/`, `hotfix/`, `refactor/`, `docs/`, `test/`
