# AGENTS.md - AI Coding Agent Guide

## Project Overview

AI Lightroom - AI-powered image color adjustment tool:
- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: React 18 with Vite 5 and Tailwind CSS 3
- **AI**: Google Gemini API for vision and LLM capabilities

## Build, Test, and Lint Commands

### Backend (Python/FastAPI)

```bash
cd api                                    # Navigate to backend directory
uv venv                                   # Create virtual environment
source .venv/bin/activate                 # Activate virtual environment (Linux/Mac)
# or .venv\Scripts\activate               # Activate virtual environment (Windows)
uv pip install -r requirements.txt       # Install dependencies
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # Run dev server

pytest                                    # Run all tests
pytest tests/test_main.py                 # Run a single test file
pytest tests/test_main.py::test_root      # Run a single test function
pytest -v                                 # Run tests with verbose output
pytest --cov=app tests/                   # Run tests with coverage

black .                                   # Format code
ruff .                                    # Lint code
mypy .                                    # Type check
```

### Frontend (React/Vite)

```bash
cd web                                    # Navigate to frontend directory
npm install                               # Install dependencies
npm run dev                               # Run development server
npm run build                             # Build for production
npm run lint                              # Run linter
npm run test                              # Run tests
npm run test -- path/to/test.test.js      # Run a single test file
```

### Docker

```bash
docker-compose up --build                 # Build and run all services
docker-compose up -d                      # Run in detached mode
docker-compose down                       # Stop services
docker-compose logs -f                    # View logs
```

## Code Style Guidelines

### Python

**Formatting (Black)**: Line length 88, double quotes for strings
**Linting (Ruff)**: PEP 8 compliant, line length 88
**Type Hints (mypy)**: Strict mode, all functions must have type hints

**Import Order**:
```python
# Standard library imports
import os
from typing import List, Dict

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local imports
from app.config import settings
from app.services.image_analyzer import ImageAnalyzer
```

**Naming Conventions**:
- Files: `snake_case.py` (e.g., `image_analyzer.py`)
- Classes: `PascalCase` (e.g., `ImageAnalyzer`)
- Functions/variables: `snake_case` (e.g., `analyze_image`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_UPLOAD_SIZE`)
- Private methods: `_leading_underscore` (e.g., `_process_image`)

**Error Handling**:
```python
from fastapi import HTTPException

if not image:
    raise HTTPException(status_code=400, detail="Image not provided")

try:
    result = process_image(image)
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

**Async/Await**: Use async for all I/O operations, `aiofiles` for async file operations

**Pydantic Models**:
```python
from pydantic import BaseModel, Field

class ColorPreset(BaseModel):
    brightness: float = Field(ge=-1.0, le=1.0, description="Brightness adjustment")
    contrast: float = Field(ge=-1.0, le=1.0, description="Contrast adjustment")
```

### JavaScript/TypeScript

**Formatting (Prettier)**: 2 space indentation, single quotes, semicolons required
**Linting (ESLint)**: React and TypeScript plugins enabled

**Import Order**:
```javascript
// React imports
import React, { useState, useEffect } from 'react';
// Third-party imports
import axios from 'axios';
import { Upload } from 'lucide-react';
// Local imports
import { analyzeImage } from '../services/api';
```

**Naming Conventions**:
- Files: `PascalCase.jsx` for components (e.g., `ImageUploader.jsx`)
- Components: `PascalCase` (e.g., `ImageUploader`)
- Functions: `camelCase` (e.g., `handleSubmit`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_FILE_SIZE`)

**Error Handling**:
```javascript
try {
  const response = await analyzeImage(file);
  setData(response.data);
} catch (error) {
  if (error.response) {
    setError(error.response.data.detail);
  } else {
    setError('An unexpected error occurred');
  }
}
```

## Project Structure

```
ai-lightroom/
├── api/                    # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py        # Application entry point
│   │   ├── config.py      # Configuration
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── schemas/       # Pydantic models
│   │   └── middleware/    # Custom middleware
│   ├── tests/             # Test suite
│   └── requirements.txt   # Dependencies
├── web/                    # Frontend (React)
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   ├── hooks/         # Custom hooks
│   │   └── utils/         # Utilities
│   └── package.json       # Dependencies
├── plans/                  # Planning documentation
├── config/                 # Shared configuration
└── scripts/                # Utility scripts
```

## Documentation Standards

### Python Docstrings
```python
def analyze_image(image_path: str) -> Dict[str, Any]:
    """
    Analyze an image and extract color information.
    
    Args:
        image_path: Path to the image file.
    
    Returns:
        Dictionary containing histogram and color data.
    
    Raises:
        ValueError: If image file is invalid.
    """
```

### JavaScript Comments
```javascript
/**
 * Validates file size and type before upload.
 * @param {File} file - The file to validate
 * @returns {boolean} True if valid, throws error if invalid
 */
const validateFile = (file) => {
  // Implementation
};
```

## Testing Guidelines

### Python Tests
- Use pytest framework, place tests in `tests/` directory
- Name test files as `test_*.py`, test functions as `test_*`
- Use fixtures for common setup, aim for >80% code coverage

### Frontend Tests
- Use Vitest (when implemented), place tests next to components as `*.test.js`
- Test user interactions, not implementation details

## Environment Variables

Backend (`.env`):
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
GOOGLE_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:5173
```

Frontend (`.env`):
```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

## Git Workflow

- **Branch naming**: `feature/description`, `bugfix/description`, `hotfix/description`
- **Commit messages**: Clear, descriptive, in present tense
- **Pull requests**: Include description, tests, and documentation updates
- **Code review**: Required before merging

## Performance Targets

- Image upload: < 1s (10MB file)
- Image analysis: < 2s
- LLM processing: < 5s
- Total end-to-end: < 10s
- API P95 latency: < 8s

## Security Considerations

- Never commit API keys or secrets
- Validate all inputs at multiple layers
- Use environment variables for configuration
- Implement rate limiting (60 requests/minute per IP)
- Sanitize logs to exclude sensitive data
- Delete uploaded images after processing

## Important Notes

- This project is in the planning phase - most code is yet to be implemented
- Follow the extensive planning documentation in `/plans/` directory
- Check task documentation in `/plans/sprint-*/tasks/` for implementation details
- Run linters and tests before committing
- Update documentation when adding new features
