# AI Lightroom Backend

FastAPI backend for AI-powered image color adjustment.

## Setup

### Prerequisites

- Python 3.11+
- uv

### Installation

```bash
# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your Gemini API key
```

### Running

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest tests/test_main.py -v
```

### Code Quality

```bash
# Format code
black app tests

# Lint code
ruff check app tests

# Type check
mypy app
```

## Project Structure

```
api/
├── app/
│   ├── main.py           # FastAPI application
│   ├── config.py         # Configuration
│   ├── routes/           # API endpoints
│   ├── services/         # Business logic
│   ├── schemas/          # Pydantic models
│   └── middleware/       # Custom middleware
├── tests/                # Test suite
├── requirements.txt      # Dependencies
└── .env.example          # Environment template
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint |
| `/health/` | GET | Health check |
| `/docs` | GET | OpenAPI documentation |
| `/api/v1/analyze` | POST | Analyze image and generate preset |

## Environment Variables

See [.env.example](./.env.example) for all configuration options.

Required:
- `GOOGLE_API_KEY` - Gemini API key

## Troubleshooting

### Import errors
Ensure you're in the `api` directory and virtual environment is activated.

### Port already in use
Change port with `--port 8001` or stop conflicting process.

### API key errors
Verify `GOOGLE_API_KEY` is set correctly in `.env`.
