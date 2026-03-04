# Technology Stack

Comprehensive overview of all technologies, libraries, and tools used in AI Lightroom with rationale for each choice.

## Backend Stack

### Core Framework

**Python 3.11+**
- **Why**: Excellent ML/AI ecosystem, async support, type hints
- **Alternatives Considered**: Node.js (less mature ML), Go (fewer libraries)
- **Decision**: Python is the de facto standard for ML and has excellent async support in 3.11+

**FastAPI 0.104+**
- **Why**: Fast (Starlette), async support, automatic OpenAPI docs, Pydantic integration
- **Alternatives Considered**: Django (too heavy), Flask (less features), Express (JavaScript)
- **Decision**: Best balance of performance, features, and developer experience for API-first projects

**Uvicorn 23.0+**
- **Why**: Lightning-fast ASGI server, production-ready, asyncio support
- **Alternatives Considered**: Gunicorn (WSGI only), Hypercorn (less popular)
- **Decision**: Standard ASGI server for FastAPI with excellent performance

### Dependencies

```python
# Core
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
pydantic>=2.5.0
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

### AI/ML Libraries

**Google Generative AI SDK 0.3.0+**
- **Why**: Official SDK for Gemini API, excellent documentation
- **Models Used**:
  - `gemini-1.5-pro-vision`: Vision API for image understanding
  - `gemini-1.5-pro`: LLM for text generation and settings
- **Alternatives Considered**: OpenAI (more expensive), Anthropic (no vision API in chosen model)
- **Decision**: Cost-effective, good balance of vision and text capabilities

### Image Processing Libraries

**OpenCV 4.8.0+ (headless)**
- **Why**: Fast, comprehensive, Python bindings, industry standard
- **Features Used**:
  - Image loading and manipulation
  - Histogram calculation
  - Color space conversions
  - Face detection (Haar cascades)
- **Alternatives Considered**: scikit-image (slower), Pillow only (less features)
- **Decision**: Best performance and feature set for image analysis

**Pillow 10.1.0+**
- **Why**: Python Imaging Library fork, excellent format support
- **Features Used**:
  - Image format validation
  - File loading and saving
  - EXIF data extraction (future)
- **Alternatives Considered**: Wand (ImageMagick), OpenCV only
- **Decision**: Complements OpenCV, better for format handling

**NumPy 1.26.0+**
- **Why**: Fast numerical operations, array processing
- **Features Used**:
  - Histogram calculations (vectorized)
  - Image array manipulation
  - Statistical calculations
- **Alternatives Considered**: Pandas (overhead), pure Python (slow)
- **Decision**: Essential for efficient image processing

### Utility Libraries

**aiofiles 23.2.1+**
- **Why**: Async file operations, integrates with async/await
- **Usage**: Async image reading and temporary file operations

**tenacity 8.2.3+**
- **Why**: Robust retry logic, exponential backoff, retry conditions
- **Usage**: Retry Gemini API calls with exponential backoff

### Development Tools

**pytest 7.4.0+**
- **Why**: Popular, powerful, plugin ecosystem
- **Features**: Async support, fixtures, parametrized tests

**pytest-asyncio 0.21.0+**
- **Why**: Async test support for pytest
- **Usage**: Test async endpoints and services

**black 23.11.0+**
- **Why**: Code formatter, consistent style, PEP 8 compliant
- **Configuration**: Line length 88, quotes double

**ruff 0.1.6+**
- **Why**: Fast linter (10x faster than flake8), compatible with black
- **Configuration**: PEP 8 compliance, line length 88

**mypy 1.7.0+**
- **Why**: Static type checking, catches bugs early
- **Configuration**: Strict mode, ignore certain external libraries

### Production Tools

**gunicorn 21.2.0+**
- **Why**: Production WSGI/ASGI server, worker management
- **Usage**: Multiple worker processes for production

**prometheus-client 0.19.0+ (Optional)**
- **Why**: Metrics collection, monitoring integration
- **Usage**: Track API metrics, performance data

## Frontend Stack

### Core Framework

**React 18.2+**
- **Why**: Component-based, large ecosystem, excellent tooling
- **Alternatives Considered**: Vue (less familiar to team), Angular (too complex)
- **Decision**: Team expertise, industry standard, great DX

**Vite 5.0+**
- **Why**: Fast HMR, optimized builds, modern tooling
- **Alternatives Considered**: Webpack (complex), Create React App (slow)
- **Decision**: Best development experience and build performance

**TypeScript 5.3+**
- **Why**: Type safety, better IDE support, catches bugs
- **Alternatives Considered**: JavaScript (no type safety), Flow (declining)
- **Decision**: Industry best practice, improves code quality

### Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "typescript": "^5.3.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.0"
  }
}
```

### UI Libraries

**Axios 1.6.0+**
- **Why**: Promise-based, interceptors, automatic JSON transformation
- **Usage**: API client for backend communication
- **Alternatives Considered**: Fetch API (boilerplate), ky (smaller ecosystem)
- **Decision**: Mature, excellent error handling, request/response interceptors

**Tailwind CSS 3.3.0+**
- **Why**: Utility-first, consistent design, responsive utilities
- **Features Used**:
  - Responsive design (mobile-first)
  - Flexbox and grid layouts
  - Color system
  - Spacing and typography utilities
- **Alternatives Considered**: CSS modules (more CSS to write), styled-components (JS styling)
- **Decision**: Faster development, smaller bundle, consistent design system

**Lucide React 0.294.0+**
- **Why**: Clean icon design, tree-shakeable, React components
- **Features Used**:
  - Upload icon
  - Copy icon
  - Loading spinner
  - Error icons
- **Alternatives Considered**: Material Icons (heavier), Heroicons (fewer icons)
- **Decision**: Modern design, excellent tree-shaking, consistent look

### Testing Tools

**Vitest 1.0.0+ (Optional)**
- **Why**: Fast, Jest-compatible, Vite integration
- **Usage**: Unit tests for components and utilities

**Testing Library 14.0.0+ (Optional)**
- **Why**: User-centric testing, encourages accessible components
- **Usage**: React component testing

**Playwright 1.40.0+ (Optional)**
- **Why**: Cross-browser, fast, reliable E2E testing
- **Usage**: End-to-end testing of user flows

### Code Quality

**ESLint 8.55.0+**
- **Why**: JavaScript/TypeScript linting, catches errors
- **Configuration**: React plugin, TypeScript rules

**Prettier 3.1.0+ (Optional)**
- **Why**: Code formatter, consistent style
- **Integration**: ESLint plugin for Prettier

## DevOps & Infrastructure

### Containerization

**Docker 24.0+**
- **Why**: Containerization, consistent environments
- **Features Used**:
  - Multi-stage builds (optimization)
  - Health checks
  - Volume mounts for development

**Docker Compose 2.21.0+**
- **Why**: Multi-container orchestration, development environment
- **Usage**: Local development with backend and frontend containers

### Web Server (Production)

**Nginx 1.25+ (Optional)**
- **Why**: High performance, reverse proxy, static file serving
- **Features Used**:
  - Reverse proxy to FastAPI
  - SSL/TLS termination
  - Static file serving for React build
  - Gzip compression

**Caddy 2.7+ (Alternative)**
- **Why**: Automatic HTTPS, simple configuration
- **Decision**: Nginx more established, Caddy easier SSL

### Monitoring (Optional)

**Prometheus 2.48.0+**
- **Why**: Metrics collection, time-series database
- **Usage**: Track API metrics, resource usage

**Grafana 10.2.0+**
- **Why**: Visualization, dashboards
- **Usage**: Monitor API health, performance

**Sentry 7.95.0+ (Optional)**
- **Why**: Error tracking, crash reporting
- **Usage**: Track production errors, alerting

### CI/CD (Optional)

**GitHub Actions**
- **Why**: Native GitHub integration, free for public repos
- **Usage**:
  - Run tests on push
  - Build Docker images
  - Deploy to production

**GitLab CI (Alternative)**
- **Why**: Built-in GitLab features
- **Decision**: Using GitHub, GitHub Actions is natural choice

## Development Tools

### Version Control

**Git**
- **Why**: Distributed version control, industry standard
- **Usage**: Version control, branching, collaboration

**GitHub**
- **Why**: Repository hosting, issue tracking, Actions
- **Usage**: Code hosting, CI/CD, project management

### Code Quality

**Pre-commit 3.5.0+ (Optional)**
- **Why**: Git hooks, run checks before commit
- **Usage**: Run black, ruff, mypy before commits

**Black**
- **Why**: Python code formatter
- **Configuration**: Line length 88, quotes double

**Ruff**
- **Why**: Fast Python linter
- **Configuration**: PEP 8 compliance

**ESLint**
- **Why**: JavaScript/TypeScript linter
- **Configuration**: React rules, TypeScript rules

**Prettier (Optional)**
- **Why**: Code formatter for frontend
- **Configuration**: 2 space indent, single quotes

### Documentation

**Markdown**
- **Why**: Simple, widely supported
- **Usage**: All documentation in .md files

**Swagger/OpenAPI (Auto-generated)**
- **Why**: API documentation, interactive docs
- **Usage**: FastAPI generates from code

## Environment Variables

### Backend (.env.example)

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Gemini API
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_MODEL=gemini-1.5-pro-vision
GOOGLE_MODEL_TEXT=gemini-1.5-pro

# File Upload
MAX_UPLOAD_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Logging
LOG_LEVEL=INFO

# Rate Limiting (future)
RATE_LIMIT_PER_MINUTE=60
```

### Frontend (.env.example)

```env
VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
VITE_MAX_FILE_SIZE=10485760
```

## System Requirements

### Development

**Minimum**:
- **OS**: macOS, Linux, Windows (WSL2)
- **Python**: 3.11 or higher
- **Node.js**: 18.0 or higher
- **RAM**: 8GB
- **Storage**: 2GB free space

**Recommended**:
- **OS**: macOS or Linux
- **Python**: 3.12
- **Node.js**: 20.0+
- **RAM**: 16GB
- **Storage**: 5GB free space

### Production

**Minimum**:
- **OS**: Linux (Ubuntu 22.04+)
- **RAM**: 4GB
- **CPU**: 2 cores
- **Storage**: 10GB free space
- **Network**: Stable internet connection

**Recommended**:
- **OS**: Linux (Ubuntu 22.04+)
- **RAM**: 8GB
- **CPU**: 4 cores
- **Storage**: 20GB free space
- **Network**: High-speed connection with redundancy

## Performance Targets

### API Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| Image Upload | < 1s (10MB) | Time from request to server receipt |
| Image Analysis | < 2s | OpenCV processing time |
| LLM Processing | < 5s | Gemini API response time |
| Total End-to-End | < 10s | Complete request/response |
| API P50 Latency | < 3s | Median response time |
| API P95 Latency | < 8s | 95th percentile |
| API P99 Latency | < 10s | 99th percentile |

### Concurrency

- **Target**: 50+ concurrent requests
- **Scaling**: Horizontal scaling with load balancer
- **Worker Processes**: 4-8 workers per instance

### Resource Usage

| Resource | Per Instance | Total (3 instances) |
|----------|--------------|---------------------|
| Memory | < 500MB | < 1.5GB |
| CPU | < 50% normal load | < 150% total |
| Disk I/O | Minimal | Minimal |

## Security Considerations

### Dependency Management

- **Updates**: Regular dependency updates (monthly)
- **Scanning**: Dependabot for security alerts
- **Review**: Manual review of security advisories
- **Pinning**: Pin major versions in requirements.txt

### API Security

- **Rate Limiting**: 60 requests/minute per IP
- **Input Validation**: Validate all inputs at multiple layers
- **File Validation**: MIME type, size, format checks
- **CORS**: Restrict to allowed origins

### Data Security

- **No Persistent Storage**: Images deleted after processing
- **Temporary Files**: Automatic cleanup
- **API Keys**: Environment variables, never in code
- **Logging**: Sanitized logs, no sensitive data

### SSL/TLS

- **Development**: Optional (localhost)
- **Production**: Required (Let's Encrypt)
- **Protocol**: TLS 1.3 minimum

## Upgrade Path

### Backend

**Planned Updates**:
- FastAPI minor versions (0.104 → 0.105, etc.)
- Gemini SDK updates (follow Google's recommendations)
- Python version upgrades (3.11 → 3.12 → 3.13)

**Breaking Changes**:
- Plan for migration guides
- Maintain backward compatibility where possible
- Notify users in advance via changelog

### Frontend

**Planned Updates**:
- React minor versions (18.2 → 18.3, etc.)
- Vite updates (5.0 → 5.1, etc.)
- Tailwind CSS updates

**Breaking Changes**:
- Update documentation
- Provide upgrade guides
- Test thoroughly before release

## Technology Alternatives

### Rejected Technologies

**Django (Backend)**
- **Reason**: Too heavy for API-only use case
- **When would we use**: Full-stack app with admin panel

**Flask (Backend)**
- **Reason**: Less built-in validation/documentation
- **When would we use**: Need more flexibility than FastAPI

**OpenAI API**
- **Reason**: More expensive, user chose Gemini
- **When would we use**: Gemini unavailable

**Vue (Frontend)**
- **Reason**: Team more familiar with React
- **When would we use**: Team prefers Vue ecosystem

**Webpack (Frontend)**
- **Reason**: More complex configuration
- **When would we use**: Need advanced bundling features

---

**Document Version**: 1.0
**Last Updated**: 2024-02-27
**Owner**: Engineering Team
**Status**: Approved
