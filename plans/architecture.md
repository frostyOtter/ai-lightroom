# System Architecture

## Overview

AI Lightroom follows a modern, microservices-inspired architecture with clear separation of concerns. The system is designed for scalability, maintainability, and ease of extension.

## High-Level Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
├──────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────┐  │
│  │               Web Interface (React)                    │  │
│  │  - Image Upload  - Preferences Input  - Results Display │  │
│  │  - State Management  - Error Handling  - Copy Actions │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST
                              ↓
┌──────────────────────────────────────────────────────────────┐
│                      API Gateway (FastAPI)                   │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Routes     │  │ Middleware   │  │  Validation  │      │
│  │  - /analyze  │  │  - CORS      │  │  - Request   │      │
│  │  - /health   │  │  - Logging   │  │  - Response  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└──────────────────────────────────────────────────────────────┘
                              │
                              │ Internal Service Calls
         ┌────────────────────┴────────────────────┐
         │                                         │
         ↓                                         ↓
┌──────────────────────┐              ┌──────────────────────┐
│   ImageAnalyzer      │              │   GeminiService      │
│   Service            │              │   Service            │
├──────────────────────┤              ├──────────────────────┤
│ - Histogram Extract  │              │ - Vision API Call    │
│ - Luminance Calc     │              │ - LLM Generation     │
│ - Brightness/Contrast│              │ - Prompt Engineering │
│ - Color Detection    │              │ - JSON Parsing       │
│ - Exposure Analysis  │              │ - Retry Logic        │
└──────────────────────┘              └──────────────────────┘
         │                                         │
         └──────────────────┬──────────────────────┘
                            │
                            ↓
                  ┌─────────────────┐
                  │ ColorPreset Gen │
                  │  - Schema Valid │
                  │  - Profile Conv │
                  └─────────────────┘
                            │
                            ↓
                  ┌─────────────────┐
                  │ Response Output │
                  │  - JSON Format  │
                  └─────────────────┘
```

## Component Details

### 1. Client Layer (Frontend)

**Technology**: React 18, Vite 5, Tailwind CSS 3

**Responsibilities**:
- User interface and interaction
- State management for application state
- API communication
- Error handling and user feedback
- Responsive design

**Key Components**:
```
web/
├── src/
│   ├── components/
│   │   ├── ImageUploader/      # File upload with drag-drop
│   │   ├── PreferenceInput/    # Text input for preferences
│   │   ├── ResultsDisplay/     # ColorPreset visualization
│   │   ├── LoadingSpinner/     # Progress indicators
│   │   └── ErrorMessage/       # User-friendly error messages
│   ├── services/
│   │   └── api.js              # Axios-based API client
│   ├── hooks/
│   │   └── useImageAnalysis/  # Custom hook for API calls
│   └── context/
│       └── AppContext.jsx      # Global state management
```

**State Management**:
- React Context API for global state
- Component-level state for UI elements
- Async state with custom hooks

**Error Handling**:
- Axios interceptors for API errors
- Error boundaries for React errors
- User-friendly error messages
- Retry logic for transient errors

### 2. API Gateway (FastAPI Backend)

**Technology**: Python 3.11+, FastAPI 0.104+, Uvicorn

**Responsibilities**:
- HTTP request handling
- Request/response validation
- Authentication and authorization (future)
- Rate limiting
- CORS configuration
- Logging and monitoring

**Key Components**:
```
api/
├── app/
│   ├── main.py                # FastAPI application
│   ├── routes/
│   │   ├── analyze.py         # /api/v1/analyze endpoint
│   │   └── health.py          # /health endpoint
│   ├── middleware/
│   │   ├── cors.py            # CORS configuration
│   │   ├── logging.py         # Request logging
│   │   └── error_handler.py   # Global error handling
│   └── schemas/
│       └── color_preset.py     # Pydantic models
```

**Middleware Stack**:
1. **CORS Middleware**: Cross-origin resource sharing
2. **Logging Middleware**: Request/response logging
3. **Error Handler**: Global exception handling
4. **Rate Limiter**: Request rate limiting (future)

**Validation**:
- Pydantic schemas for all request/response models
- File type and size validation
- Input sanitization
- Schema validation with detailed errors

### 3. ImageAnalyzer Service

**Technology**: OpenCV 4.8+, NumPy 1.26+, Pillow 10.1+

**Responsibilities**:
- Image loading and validation
- Histogram extraction (R, G, B channels)
- Luminance calculation
- Brightness and contrast measurement
- Dominant color detection
- Exposure analysis (over/under-exposed)
- Face detection (optional)

**Architecture**:
```
api/
└── services/
    └── image_analyzer/
        ├── __init__.py
        ├── analyzer.py          # Main analyzer class
        ├── histogram.py         # Histogram extraction
        ├── luminance.py         # Luminance calculation
        ├── colors.py            # Color detection
        ├── exposure.py          # Exposure analysis
        └── face_detection.py    # Face detection
```

**Key Methods**:
```python
class ImageAnalyzer:
    def analyze(self, image: bytes) -> ImageAnalysis:
        """Comprehensive image analysis"""

    def extract_histogram(self, image: np.ndarray) -> Histogram:
        """Extract RGB histograms"""

    def calculate_luminance(self, image: np.ndarray) -> float:
        """Calculate overall luminance"""

    def detect_dominant_colors(self, image: np.ndarray) -> List[Color]:
        """Detect top 5 dominant colors"""
```

**Performance Optimizations**:
- Image resizing for faster processing
- NumPy vectorization for histogram calculation
- Caching for repeated analyses
- Async I/O for file operations

### 4. GeminiService Service

**Technology**: Google Generative AI SDK, Gemini 1.5 Pro Vision

**Responsibilities**:
- Vision API integration for image understanding
- LLM API integration for color setting generation
- Prompt engineering and management
- JSON output parsing and validation
- Retry logic and rate limiting
- Error handling and logging

**Architecture**:
```
api/
└── services/
    └── gemini_service/
        ├── __init__.py
        ├── client.py            # Gemini client wrapper
        ├── prompts.py           # Prompt templates
        ├── parser.py            # JSON response parser
        ├── validator.py         # Schema validation
        └── retry_handler.py     # Retry logic
```

**Key Methods**:
```python
class GeminiService:
    def generate_preset(
        self,
        image: bytes,
        preferences: str,
        analysis: ImageAnalysis
    ) -> ColorPreset:
        """Generate complete ColorPreset"""

    def generate_with_vision(
        self,
        image: bytes,
        preferences: str
    ) -> dict:
        """Generate using Vision API"""

    def validate_response(
        self,
        response: dict
    ) -> ColorPreset:
        """Validate and parse response"""
```

**Prompt Engineering**:
- System prompt for color expertise
- Few-shot examples for consistency
- Image analysis integration
- JSON schema enforcement
- Style preference handling

### 5. ExportConverter Service

**Technology**: Python utilities, Pydantic

**Responsibilities**:
- Convert normalized values to Lightroom scale
- Generate export profiles
- Support future export formats
- Value range transformations

**Architecture**:
```
api/
└── services/
    └── export_converter/
        ├── __init__.py
        ├── converter.py         # Main converter
        ├── lightroom.py         # Lightroom conversions
        └── generic.py           # Generic normalized
```

**Key Methods**:
```python
class ExportConverter:
    def to_lightroom(
        self,
        preset: ColorPreset
    ) -> LightroomProfile:
        """Convert to Lightroom scale"""

    def to_generic(
        self,
        preset: ColorPreset
    ) -> GenericProfile:
        """Keep normalized values"""

    def convert_value(
        self,
        value: float,
        from_range: tuple,
        to_range: tuple
    ) -> float:
        """Generic value conversion"""
```

## Data Flow

### Complete Request Flow

```
1. User Uploads Image
   ↓
2. Frontend: ImageUploader validates file
   ↓
3. Frontend: API client sends POST /api/v1/analyze
   ↓
4. FastAPI: Validates request (multipart/form-data)
   ↓
5. FastAPI: Routes to analyze endpoint
   ↓
6. FastAPI: Calls ImageAnalyzer.analyze(image)
   ├─ Histogram extraction
   ├─ Luminance calculation
   ├─ Color detection
   └─ Exposure analysis
   ↓
7. FastAPI: Calls GeminiService.generate_preset()
   ├─ Sends image to Vision API
   ├─ Sends preferences and analysis to LLM
   └─ Receives ColorPreset JSON
   ↓
8. FastAPI: Validates ColorPreset with Pydantic
   ↓
9. FastAPI: Calls ExportConverter for export profiles
   ├─ Lightroom profile
   └─ Generic profile
   ↓
10. FastAPI: Returns response with ColorPreset
    ↓
11. Frontend: Displays results in ResultsDisplay
    └─ User can copy or download JSON
```

### Error Handling Flow

```
Error Detected
   ↓
Service Layer catches exception
   ↓
Logs error details
   ↓
Maps to error code (e.g., INVALID_FILE_FORMAT)
   ↓
Returns structured error response
   ↓
Frontend intercepts error
   ↓
Displays user-friendly message in ErrorMessage
   ↓
Provides retry option if applicable
```

## Security Architecture

### Input Validation
- File type validation (MIME type)
- File size limits (10MB max)
- Input sanitization (text preferences)
- Schema validation (Pydantic)

### API Security
- CORS configuration (restrict origins)
- Rate limiting (60 requests/minute)
- Input validation at all layers
- No sensitive data in logs

### Data Privacy
- No persistent image storage
- Temporary files deleted after processing
- API keys in environment variables
- No personal data collection

### Future Security
- API key authentication
- OAuth 2.0 for user accounts
- Encryption at rest
- Audit logging

## Scalability Architecture

### Horizontal Scaling
```
                        Load Balancer
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ↓                    ↓                    ↓
    FastAPI Instance 1   FastAPI Instance 2   FastAPI Instance 3
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                              ↓
                      Shared Cache (Redis)
                              │
                              ↓
                    Gemini API (External)
```

### Caching Strategy
- Cache repeated image analyses
- Cache prompt responses
- TTL-based cache expiration
- Cache invalidation on updates

### Async Processing
- Async/await for I/O operations
- Background tasks for heavy processing
- Queue system for batch operations
- WebSocket for real-time updates (future)

## Deployment Architecture

### Development
```
Docker Compose
├── Backend Container (FastAPI)
├── Frontend Container (React Dev Server)
└── Hot Reload for both
```

### Production
```
Nginx Reverse Proxy
    │
    ├─→ Static Files (React build)
    └─→ API Proxy (FastAPI)
         │
         ├─→ FastAPI Instance 1
         ├─→ FastAPI Instance 2
         └─→ FastAPI Instance 3
```

### Infrastructure
- **Container Orchestration**: Docker, Kubernetes (future)
- **Reverse Proxy**: Nginx/Caddy
- **SSL/TLS**: Let's Encrypt
- **Monitoring**: Prometheus + Grafana (optional)
- **Logging**: Structured logging, ELK stack (optional)

## Technology Rationale

### FastAPI
- **Pros**: Fast, async support, automatic API docs, type safety with Pydantic
- **Cons**: Smaller ecosystem than Django/Flask
- **Decision**: Best fit for API-first, performance-critical application

### React
- **Pros**: Large ecosystem, component-based, great tooling
- **Cons**: Learning curve, build complexity
- **Decision**: Team familiarity, excellent for UI-heavy applications

### OpenCV
- **Pros**: Fast, comprehensive image processing, Python bindings
- **Cons**: Large dependency
- **Decision**: Industry standard, excellent performance

### Gemini API
- **Pros**: Vision + LLM in one API, cost-effective, good documentation
- **Cons**: Newer than competitors, rate limits
- **Decision**: User preference, good balance of features and cost

## Monitoring & Observability

### Metrics to Track
- API response times (P50, P95, P99)
- Error rates by endpoint
- User activity (uploads, generations)
- Resource usage (CPU, memory, disk)
- Gemini API usage and costs

### Logging Strategy
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request/response logging (sanitized)
- Error stack traces
- Performance metrics

### Health Checks
- /health endpoint
- Database connectivity (future)
- External API health
- Disk space monitoring

## Future Architecture Enhancements

### Phase 2 Enhancements
- Message queue for batch processing
- Database for user accounts and presets
- CDN for static assets
- Image processing service (apply settings to images)

### Phase 3 Enhancements
- WebSocket for real-time preview
- Video processing service
- Plugin architecture for custom exporters
- Microservices decomposition

---

**Document Version**: 1.0
**Last Updated**: 2024-02-27
**Owner**: Architecture Team
**Status**: Approved
