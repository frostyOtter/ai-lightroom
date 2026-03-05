# Task 02: Setup Python Backend Environment

**Task ID**: sprint-0-t02
**Task Name**: Setup Python Backend Environment
**Sprint**: 0
**Priority**: High
**Estimated Time**: 3 hours
**Assigned To**: [Backend Developer]

---

## 1. Objective

Set up a complete Python development environment for the FastAPI backend with all required dependencies, proper project structure, and a running development server.

## 2. Why This Matters

### Business Value
- **Backend Core**: All AI processing happens here - must be reliable
- **Development Speed**: Proper setup enables rapid iteration
- **Team Productivity**: Consistent environment prevents time-wasting setup issues

### Technical Value
- **FastAPI Benefits**: Async support, automatic API docs, type safety
- **Pydantic Validation**: Data validation and serialization
- **Modern Python**: Latest Python features and best practices

### Risks of Not Doing This
- **Development Blocked**: Without backend setup, Sprint 1 cannot begin
- **Environment Issues**: Different versions cause bugs
- **Lost Time**: Manual setup repeated for each developer

## 3. Dependencies

### Prerequisites
- [x] t01-init-repo (repository structure exists)
- [x] Python 3.11+ installed locally
- [x] pip (Python package manager) available

### Blocking
- [ ] t04-docker-config (depends on backend setup)
- [ ] t05-env-config (depends on backend setup)
- [ ] Sprint 1 backend tasks (cannot start without this)

### External Dependencies
- FastAPI, Uvicorn, Pydantic (PyPI packages)
- Gemini API access (will configure in t05)

## 4. Acceptance Criteria

### Definition of Done
- [x] Python virtual environment created
- [x] requirements.txt with all dependencies
- [x] FastAPI application structure created
- [x] Basic FastAPI app runs without errors
- [x] Health check endpoint returns 200 OK
- [x] Auto-reload enabled for development
- [x] API documentation accessible at /docs

### Success Metrics
- Server starts in < 3 seconds
- Health check responds in < 100ms
- No errors in console output
- /docs page renders correctly

### Edge Cases to Handle
- Python version not 3.11+
- pip install fails (network issues)
- Virtual environment activation issues
- Port 8000 already in use

## 5. Technical Implementation

### Approach

1. Create Python virtual environment
2. Install all required dependencies
3. Create FastAPI application structure
4. Implement basic endpoints
5. Configure development settings
6. Test server startup and endpoints

### Key Dependencies

**requirements.txt**
```text
# Core FastAPI
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6

# Data Validation
pydantic>=2.5.0

# Configuration
python-dotenv>=1.0.0

# AI/ML
google-generativeai>=0.3.0

# Image Processing
opencv-python-headless>=4.8.0
Pillow>=10.1.0
numpy>=1.26.0

# Utilities
aiofiles>=23.2.1
tenacity>=8.2.3

# Development
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.11.0
ruff>=0.1.6
mypy>=1.7.0
```

### Project Structure

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── routes/
│   │   ├── __init__.py
│   │   └── health.py        # Health check endpoint
│   ├── services/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   └── middleware/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── requirements.txt
├── .env.example
└── .gitkeep
```

### Implementation Files

**api/app/main.py**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health
from app.config import settings

app = FastAPI(
    title="AI Lightroom API",
    description="AI-powered image color adjustment API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])

@app.get("/")
async def root():
    return {
        "message": "AI Lightroom API",
        "version": "1.0.0",
        "status": "running"
    }

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    print("🚀 AI Lightroom API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    print("👋 AI Lightroom API shutting down...")
```

**api/app/config.py**
```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000"
    ]
    
    # Gemini API (placeholder)
    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL: str = "gemini-1.5-pro-vision"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

**api/app/routes/health.py**
```python
from fastapi import APIRouter, HTTPException
from typing import Dict

router = APIRouter()

@router.get("/", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "ai-lightroom-api"
    }

@router.get("/detailed", response_model=Dict[str, any])
async def detailed_health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": "ai-lightroom-api",
        "components": {
            "database": "not configured",
            "gemini_api": "not configured"
        }
    }
```

**api/.env.example**
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_MODEL=gemini-1.5-pro-vision

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# File Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp
```

**api/tests/test_main.py**
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["status"] == "running"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
```

### Pseudocode / Algorithm

```bash
# Step 1: Navigate to api directory
cd api

# Step 2: Create virtual environment
python3 -m venv venv

# Step 3: Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Step 4: Upgrade pip
pip install --upgrade pip

# Step 5: Install dependencies
pip install -r requirements.txt

# Step 6: Create application structure
mkdir -p app/{routes,services,schemas,middleware}
mkdir -p tests

# Step 7: Create Python files (see above)
# Create __init__.py files
# Create main.py, config.py
# Create health endpoint

# Step 8: Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Step 9: Test endpoints
# Open http://localhost:8000 in browser
# Open http://localhost:8000/docs for API docs
```

## 6. Testing Strategy

### Unit Tests

**Test Cases**:
- [x] test_root - Root endpoint returns correct data
- [x] test_health_check - Health endpoint returns healthy status

**Test Coverage Target**: 100% for endpoints created

### Manual Testing

**Steps**:
1. Navigate to api directory
2. Activate virtual environment
3. Run `uvicorn app.main:app --reload --port 8000`
4. Open http://localhost:8000 - should see JSON response
5. Open http://localhost:8000/health - should see healthy status
6. Open http://localhost:8000/docs - should see API documentation
7. Modify code - server should auto-reload

**Expected Results**:
- Server starts without errors
- All endpoints return 200 OK
- API docs page renders correctly
- Auto-reload works on file changes

### Performance Testing

**Benchmarks**:
- Startup time: < 3 seconds
- Health check response: < 100ms
- Memory usage: < 100MB idle

## 7. Checklist

### Implementation
- [x] Create virtual environment
- [x] Create requirements.txt
- [x] Install dependencies
- [x] Create application structure
- [x] Create main.py with FastAPI app
- [x] Create config.py with settings
- [x] Create health check endpoint
- [x] Create .env.example
- [x] Create basic test file

### Code Quality
- [x] Follow PEP 8 style guide
- [x] Add docstrings to functions
- [x] Use type hints
- [x] Organize imports

### Testing
- [x] Write unit tests
- [x] Run tests with pytest
- [x] Test server startup
- [x] Test all endpoints
- [x] Test auto-reload

### Documentation
- [x] Add comments to code
- [x] Document configuration options
- [x] Update README with setup instructions
- [x] Document API endpoints

### Review
- [x] Self-review code
- [ ] Get peer review
- [ ] Address review feedback
- [ ] Final code review

## 8. Resources & References

**Documentation**:
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)

**Tools & Libraries**:
- FastAPI - Modern Python web framework
- Uvicorn - Lightning-fast ASGI server
- Pydantic - Data validation using Python type annotations

**Helpful Articles**:
- [FastAPI Project Structure](https://fastapi.tiangolo.com/tutorial/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Async Python Programming](https://docs.python.org/3/library/asyncio.html)

## 9. Common Issues & Solutions

**Issue 1**: Module not found error when importing app modules
- **Solution**: Ensure PYTHONPATH includes api directory or run from api directory
- **Prevention**: Use relative imports and proper package structure

**Issue 2**: Port 8000 already in use
- **Solution**: Use different port with `--port 8001` or kill process using port
- **Prevention**: Document port usage, use environment variables

**Issue 3**: pip install fails due to network issues
- **Solution**: Use pip with `--default-timeout=1000` or try again
- **Prevention**: Use requirements.txt with version pinning

**Issue 4**: Virtual environment not activating
- **Solution**: Check Python path, try full path to activate script
- **Prevention**: Document exact activation commands for each OS

## 10. Time Tracking

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Create venv | 10 min | | |
| Install dependencies | 15 min | | |
| Create structure | 15 min | | |
| Implement main.py | 30 min | | |
| Implement config.py | 15 min | | |
| Implement health endpoint | 15 min | | |
| Create tests | 20 min | | |
| Test everything | 20 min | | |
| **Total** | **2.5 hrs** | | |

## 11. Notes

**Development Workflow**:

1. Activate virtual environment
2. Make code changes
3. Server auto-reloads (with --reload flag)
4. Test changes
5. Run tests (`pytest`)
6. Commit changes

**Future Enhancements**:
- Add logging configuration
- Add middleware for request logging
- Add exception handling
- Add database models (when needed)
- Add authentication middleware

---

**Task Status**: 🔴 Not Started
**Last Updated**: 2024-02-27
**Reviewer**: [Name]
