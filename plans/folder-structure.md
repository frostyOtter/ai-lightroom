# Project Folder Structure

Complete folder structure for the AI Lightroom project. This structure is designed for scalability, maintainability, and clarity.

## 📁 Complete Structure

```
ai-lightroom/                           # Root directory
│
├── api/                                # Backend (FastAPI)
│   ├── app/                            # Application code
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── config.py                   # Configuration management
│   │   │
│   │   ├── routes/                     # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── health.py               # Health check endpoints
│   │   │   └── analyze.py              # Image analysis endpoint
│   │   │
│   │   ├── services/                   # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── image_analyzer/         # Image analysis service
│   │   │   │   ├── __init__.py
│   │   │   │   ├── analyzer.py         # Main analyzer
│   │   │   │   ├── histogram.py        # Histogram extraction
│   │   │   │   ├── luminance.py        # Luminance calculation
│   │   │   │   ├── colors.py           # Color detection
│   │   │   │   ├── exposure.py         # Exposure analysis
│   │   │   │   └── face_detection.py   # Face detection
│   │   │   │
│   │   │   ├── gemini_service/         # Gemini AI service
│   │   │   │   ├── __init__.py
│   │   │   │   ├── client.py           # Gemini client
│   │   │   │   ├── prompts.py          # Prompt templates
│   │   │   │   ├── parser.py           # JSON parser
│   │   │   │   ├── validator.py        # Schema validation
│   │   │   │   └── retry_handler.py    # Retry logic
│   │   │   │
│   │   │   └── export_converter/       # Export format conversion
│   │   │       ├── __init__.py
│   │   │       ├── converter.py        # Main converter
│   │   │       ├── lightroom.py        # Lightroom format
│   │   │       └── generic.py          # Generic format
│   │   │
│   │   ├── schemas/                    # Pydantic models
│   │   │   ├── __init__.py
│   │   │   ├── color_preset.py         # ColorPreset schema
│   │   │   ├── requests.py             # Request models
│   │   │   └── responses.py            # Response models
│   │   │
│   │   └── middleware/                 # Custom middleware
│   │       ├── __init__.py
│   │       ├── cors.py                 # CORS configuration
│   │       ├── logging.py              # Request logging
│   │       └── error_handler.py        # Error handling
│   │
│   ├── tests/                          # Test suite
│   │   ├── __init__.py
│   │   ├── conftest.py                 # Pytest configuration
│   │   ├── test_main.py
│   │   ├── test_routes/
│   │   │   ├── test_health.py
│   │   │   └── test_analyze.py
│   │   ├── test_services/
│   │   │   ├── test_image_analyzer.py
│   │   │   └── test_gemini_service.py
│   │   └── test_schemas/
│   │       └── test_color_preset.py
│   │
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                   # Environment variables template
│   ├── Dockerfile                      # Backend container
│   ├── README.md                       # Backend documentation
│   └── pyproject.toml                  # Python project config (optional)
│
├── web/                                # Frontend (React)
│   ├── src/                            # Source code
│   │   ├── main.jsx                    # Entry point
│   │   ├── App.jsx                     # Root component
│   │   ├── index.css                   # Global styles
│   │   │
│   │   ├── components/                 # React components
│   │   │   ├── ImageUploader/
│   │   │   │   ├── index.jsx
│   │   │   │   ├── ImageUploader.jsx
│   │   │   │   └── ImageUploader.css
│   │   │   ├── PreferenceInput/
│   │   │   │   ├── index.jsx
│   │   │   │   ├── PreferenceInput.jsx
│   │   │   │   └── PreferenceInput.css
│   │   │   ├── ResultsDisplay/
│   │   │   │   ├── index.jsx
│   │   │   │   ├── ResultsDisplay.jsx
│   │   │   │   └── ResultsDisplay.css
│   │   │   ├── LoadingSpinner/
│   │   │   │   ├── index.jsx
│   │   │   │   ├── LoadingSpinner.jsx
│   │   │   │   └── LoadingSpinner.css
│   │   │   └── ErrorMessage/
│   │   │       ├── index.jsx
│   │   │       ├── ErrorMessage.jsx
│   │   │       └── ErrorMessage.css
│   │   │
│   │   ├── services/                   # API and utility services
│   │   │   └── api.js                  # Axios-based API client
│   │   │
│   │   ├── hooks/                      # Custom React hooks
│   │   │   └── useImageAnalysis.js    # Image analysis hook
│   │   │
│   │   ├── context/                    # React Context providers
│   │   │   └── AppContext.jsx          # Global app state
│   │   │
│   │   ├── utils/                      # Utility functions
│   │   │   ├── validators.js           # Input validation
│   │   │   └── formatters.js           # JSON formatting
│   │   │
│   │   └── styles/                     # Styling configuration
│   │       └── tailwind.config.js      # Tailwind config
│   │
│   ├── public/                         # Static assets
│   │   ├── favicon.ico
│   │   └── logo.svg                    # Optional
│   │
│   ├── package.json                    # Node dependencies
│   ├── vite.config.js                  # Vite configuration
│   ├── tailwind.config.js              # Tailwind configuration
│   ├── postcss.config.js               # PostCSS configuration
│   ├── .env.example                    # Environment variables template
│   ├── Dockerfile                      # Frontend container
│   ├── README.md                       # Frontend documentation
│   └── tsconfig.json                   # TypeScript config (if using TS)
│
├── plans/                              # Project planning documents
│   ├── README.md                       # Sprint planning overview
│   ├── project-overview.md             # Project vision and goals
│   ├── architecture.md                 # System architecture
│   ├── tech-stack.md                   # Technology choices
│   ├── folder-structure.md             # This file
│   │
│   ├── shared/                         # Shared planning resources
│   │   ├── task-template.md            # Task documentation template
│   │   ├── schema-reference.md         # ColorPreset schema reference
│   │   └── api-endpoints.md            # Complete API documentation
│   │
│   ├── sprint-0/                       # Sprint 0: Project Setup
│   │   ├── README.md                   # Sprint overview
│   │   ├── goals.md                    # Sprint goals
│   │   ├── checklist.md                 # Sprint checklist
│   │   ├── deliverables.md             # Deliverables
│   │   └── tasks/
│   │       ├── t01-init-repo.md
│   │       ├── t02-setup-python.md
│   │       ├── t03-setup-frontend.md
│   │       ├── t04-docker-config.md
│   │       ├── t05-env-config.md
│   │       ├── t06-git-setup.md
│   │       └── t07-documentation.md
│   │
│   ├── sprint-1/                       # Sprint 1: Backend API Foundation
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-fastapi-structure.md
│   │       ├── t02-pydantic-schemas.md
│   │       ├── t03-image-upload.md
│   │       ├── t04-file-validation.md
│   │       ├── t05-health-check.md
│   │       ├── t06-gemini-setup.md
│   │       ├── t07-error-handling.md
│   │       ├── t08-cors-config.md
│   │       └── t09-api-documentation.md
│   │
│   ├── sprint-2/                       # Sprint 2: Image Analysis Engine
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-analyzer-service.md
│   │       ├── t02-histogram-extraction.md
│   │       ├── t03-luminance-calculation.md
│   │       ├── t04-brightness-contrast.md
│   │       ├── t05-dominant-colors.md
│   │       ├── t06-exposure-detection.md
│   │       ├── t07-error-handling.md
│   │       └── t08-performance-opt.md
│   │
│   ├── sprint-3/                       # Sprint 3: Gemini Integration
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-vision-api-integration.md
│   │       ├── t02-prompt-engineering.md
│   │       ├── t03-llm-generation.md
│   │       ├── t04-json-parsing.md
│   │       ├── t05-schema-validation.md
│   │       ├── t06-retry-logic.md
│   │       ├── t07-rate-limiting.md
│   │       ├── t08-logging.md
│   │       └── t09-prompt-tuning.md
│   │
│   ├── sprint-4/                       # Sprint 4: API Endpoints & Validation
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-analyze-endpoint.md
│   │       ├── t02-service-integration.md
│   │       ├── t03-request-validation.md
│   │       ├── t04-response-validation.md
│   │       ├── t05-export-converter.md
│   │       ├── t06-error-responses.md
│   │       ├── t07-request-logging.md
│   │       ├── t08-rate-limiting.md
│   │       ├── t09-openapi-spec.md
│   │       └── t10-integration-tests.md
│   │
│   ├── sprint-5/                       # Sprint 5: Frontend Development
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-react-setup.md
│   │       ├── t02-tailwind-config.md
│   │       ├── t03-layout-structure.md
│   │       ├── t04-image-uploader.md
│   │       ├── t05-preference-input.md
│   │       ├── t06-results-display.md
│   │       ├── t07-loading-states.md
│   │       ├── t08-api-client.md
│   │       ├── t09-error-handling.md
│   │       ├── t10-copy-functionality.md
│   │       └── t11-responsive-design.md
│   │
│   ├── sprint-6/                       # Sprint 6: Integration & Testing
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-api-connection.md
│   │       ├── t02-e2e-tests.md
│   │       ├── t03-performance-profiling.md
│   │       ├── t04-optimization.md
│   │       ├── t05-bug-fixes.md
│   │       ├── t06-monitoring.md
│   │       ├── t07-documentation-update.md
│   │       └── t08-user-guide.md
│   │
│   ├── sprint-7/                       # Sprint 7: Docker & Deployment
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-backend-dockerfile.md
│   │       ├── t02-frontend-dockerfile.md
│   │       ├── t03-docker-compose.md
│   │       ├── t04-multi-stage-builds.md
│   │       ├── t05-env-config.md
│   │       ├── t06-health-checks.md
│   │       ├── t07-image-optimization.md
│   │       ├── t08-deployment-docs.md
│   │       ├── t09-nginx-config.md
│   │       └── t10-ssl-configuration.md
│   │
│   ├── sprint-8/                       # Sprint 8: Refinement & Polish
│   │   ├── README.md
│   │   ├── goals.md
│   │   ├── checklist.md
│   │   ├── deliverables.md
│   │   └── tasks/
│   │       ├── t01-prompt-accuracy.md
│   │       ├── t02-example-presets.md
│   │       ├── t03-error-messages.md
│   │       ├── t04-onboarding.md
│   │       ├── t05-performance-optimization.md
│   │       ├── t06-security-audit.md
│   │       ├── t07-documentation-final.md
│   │       ├── t08-demo-materials.md
│   │       └── t09-feedback-integration.md
│   │
│   └── phase-2/                        # Future Enhancements
│       ├── README.md
│       ├── batch-processing.md
│       ├── preset-library.md
│       ├── user-accounts.md
│       └── advanced-features.md
│
├── config/                             # Shared configuration
│   ├── logging.py                      # Logging configuration
│   └── constants.py                    # Application constants
│
├── scripts/                            # Utility scripts
│   ├── setup-dev.sh                    # Development setup script
│   ├── setup-prod.sh                   # Production setup script
│   ├── lint.sh                         # Run linters
│   ├── test.sh                         # Run tests
│   └── deploy.sh                       # Deployment script
│
├── .gitignore                          # Git ignore file
├── .gitattributes                      # Git attributes
├── docker-compose.yml                  # Docker Compose configuration
├── README.md                           # Main project README
└── LICENSE                             # Project license
```

## 📋 Folder Descriptions

### Root Level Files

- **README.md**: Main project documentation and quick start guide
- **LICENSE**: MIT license file
- **.gitignore**: Files and directories to ignore in Git
- **.gitattributes**: Git configuration for line endings and merges
- **docker-compose.yml**: Multi-container Docker application definition

### /api - Backend

Contains all FastAPI backend code, including routes, services, schemas, and tests.

### /web - Frontend

Contains all React frontend code, including components, services, hooks, and context.

### /plans - Planning

Comprehensive project planning with sprint breakdowns, task documentation, and design documents.

### /config - Configuration

Shared configuration files used by both backend and frontend.

### /scripts - Utility Scripts

Automation scripts for setup, testing, linting, and deployment.

## 🎯 Naming Conventions

### Directories
- Lowercase with underscores for multi-word names (e.g., `image_analyzer`)
- Services grouped by functionality

### Files
- **Python**: Lowercase with underscores (e.g., `color_preset.py`)
- **JavaScript/JSX**: PascalCase for components (e.g., `ImageUploader.jsx`)
- **CSS**: Same name as component (e.g., `ImageUploader.css`)
- **Tests**: `test_*.py` for Python, `*.test.js` for JavaScript

### Branches
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `sprint-X` - Sprint-specific branches
- `hotfix/description` - Emergency fixes

## 🔄 Usage Guidelines

### Adding New Features

1. Create feature branch from `develop`
2. Add new files following structure conventions
3. Update documentation as needed
4. Add tests for new code
5. Submit pull request with description

### Onboarding New Developers

1. Clone repository
2. Follow README quick start guide
3. Review architecture and tech stack docs
4. Start with current sprint tasks

### Modifying Structure

Any structural changes should:
1. Be discussed with team
2. Update this document
3. Migrate existing files
4. Update all documentation

---

**Document Version**: 1.0
**Last Updated**: 2024-02-27
**Owner**: Architecture Team
**Status**: Approved
