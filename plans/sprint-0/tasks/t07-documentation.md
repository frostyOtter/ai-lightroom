# Task 07: Documentation

**Task ID**: sprint-0-t07
**Task Name**: Documentation
**Sprint**: 0
**Priority**: High
**Estimated Time**: 4 hours
**Assigned To**: [Technical Writer/Developer]

---

## 1. Objective

Create comprehensive documentation covering project setup, architecture, development guidelines, and API usage for the AI Lightroom project.

## 2. Why This Matters

### Business Value
- **Onboarding**: New team members can start quickly
- **Knowledge Transfer**: Reduces dependency on individuals
- **Professionalism**: Shows project is well-managed

### Technical Value
- **Clarity**: Reduces questions and confusion
- **Consistency**: Everyone follows same patterns
- **Maintainability**: Future developers understand decisions

### Risks of Not Doing This
- **Lost Knowledge**: When developers leave, knowledge leaves
- **Inconsistent Code**: No guidance leads to different approaches
- **Slow Onboarding**: New developers take weeks to contribute

## 3. Dependencies

### Prerequisites
- [x] t01-init-repo (repository exists)
- [x] t02-setup-python (backend ready)
- [x] t03-setup-frontend (frontend ready)
- [x] All Sprint 0 tasks (documentation covers everything)

### Blocking
- [ ] Sprint 1-8 (developers need docs to start)

### External Dependencies
- None

## 4. Acceptance Criteria

### Definition of Done
- [ ] Root README.md created with quick start
- [ ] API README.md created with backend guide
- [ ] Web README.md created with frontend guide
- [ ] CONTRIBUTING.md created
- [ ] Architecture decisions documented
- [ ] Development workflow documented
- [ ] Troubleshooting guide created
- [ ] All docs reviewed for accuracy

### Success Metrics
- New developer can set up project in < 30 minutes
- All major features documented
- All configuration options explained
- Common issues have solutions

### Edge Cases to Handle
- Different operating systems
- Different skill levels
- Different development environments

## 5. Technical Implementation

### Approach

1. Create root README.md
2. Create backend README.md
3. Create frontend README.md
4. Create CONTRIBUTING.md
5. Create troubleshooting guide
6. Review all docs

### Implementation Files

**README.md** (root)
```markdown
# AI Lightroom

AI-powered image color adjustment tool that generates professional-grade color presets from natural language descriptions.

## Features

- 🖼️ Image upload and analysis
- 🎨 Natural language style input
- 🤖 AI-powered color adjustment generation
- 📤 Export-ready Lightroom presets
- 🐳 Docker support for easy setup

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker (optional)

### Option 1: Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/username/ai-lightroom.git
cd ai-lightroom

# Copy environment files
cp .env.example .env
cp api/.env.example api/.env
cp web/.env.example web/.env

# Edit .env and add your Gemini API key
# Get your key at: https://makersuite.google.com/app/apikey

# Start services
docker-compose up
```

Open http://localhost:5173

### Option 2: Manual Setup

```bash
# Clone repository
git clone https://github.com/username/ai-lightroom.git
cd ai-lightroom

# Setup backend
cd api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your Gemini API key
uvicorn app.main:app --reload --port 8000

# In another terminal, setup frontend
cd web
npm install
cp .env.example .env
npm run dev
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

## Project Structure

```
ai-lightroom/
├── api/                 # FastAPI backend
│   ├── app/            # Application code
│   ├── tests/          # Test suite
│   └── requirements.txt
├── web/                 # React frontend
│   ├── src/            # Source code
│   └── package.json
├── plans/              # Project planning docs
└── docker-compose.yml  # Docker configuration
```

## Development

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

## Documentation

- [Project Overview](./plans/project-overview.md)
- [Architecture](./plans/architecture.md)
- [Tech Stack](./plans/tech-stack.md)
- [API Documentation](http://localhost:8000/docs) (when running)

## License

MIT License - see [LICENSE](./LICENSE)
```

**api/README.md**
```markdown
# AI Lightroom Backend

FastAPI backend for AI-powered image color adjustment.

## Setup

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

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
```

**web/README.md**
```markdown
# AI Lightroom Frontend

React frontend for AI-powered image color adjustment.

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env if needed
```

### Running

```bash
# Development mode
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Testing

```bash
# Run tests (when configured)
npm run test

# Run e2e tests (when configured)
npm run test:e2e
```

### Code Quality

```bash
# Lint code
npm run lint

# Fix lint issues
npm run lint -- --fix
```

## Project Structure

```
web/
├── src/
│   ├── main.jsx          # Entry point
│   ├── App.jsx           # Root component
│   ├── components/       # React components
│   ├── services/         # API services
│   ├── hooks/            # Custom hooks
│   └── utils/            # Utility functions
├── public/               # Static assets
├── index.html            # HTML template
└── package.json          # Dependencies
```

## Key Components

| Component | Description |
|-----------|-------------|
| `ImageUploader` | Image upload with drag-drop |
| `PreferenceInput` | Style preference text input |
| `ResultsDisplay` | Color preset visualization |
| `LoadingSpinner` | Loading indicator |
| `ErrorMessage` | Error display |

## Environment Variables

See [.env.example](./.env.example) for all options.

Required:
- `VITE_API_URL` - Backend API URL

## Troubleshooting

### Module not found
Run `npm install` to ensure all dependencies are installed.

### Port already in use
Vite will automatically use next available port.

### API connection errors
Verify `VITE_API_URL` is correct and backend is running.
```

**CONTRIBUTING.md**
```markdown
# Contributing to AI Lightroom

Thank you for your interest in contributing!

## Development Setup

See [README.md](./README.md) for setup instructions.

## Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make changes**
   - Follow code style guidelines
   - Write tests for new features
   - Update documentation

3. **Test your changes**
   ```bash
   # Backend
   cd api && pytest
   
   # Frontend
   cd web && npm run lint && npm run test
   ```

4. **Commit your changes**
   ```bash
   git commit -m "feat: add new feature"
   ```
   See [Git Workflow](./docs/git-workflow.md) for commit format.

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature
   ```

## Code Style

### Python
- Follow PEP 8
- Use Black for formatting
- Use Ruff for linting
- Add type hints

### JavaScript/React
- Use ESLint configuration
- Use Prettier for formatting
- Use functional components with hooks

## Testing

- Write unit tests for all new features
- Maintain test coverage above 80%
- Run tests before committing

## Documentation

- Update README.md if needed
- Update API docs for new endpoints
- Add JSDoc/docstrings for new functions

## Questions?

Open an issue or contact the maintainers.
```

**docs/troubleshooting.md**
```markdown
# Troubleshooting Guide

## Common Issues

### Setup Issues

#### Python version mismatch
**Problem**: Python 3.11+ required
**Solution**: Install Python 3.11 or use pyenv
```bash
pyenv install 3.11
pyenv local 3.11
```

#### Node version mismatch
**Problem**: Node.js 18+ required
**Solution**: Install Node.js 18 or use nvm
```bash
nvm install 18
nvm use 18
```

#### Docker not running
**Problem**: Docker commands fail
**Solution**: Start Docker Desktop

### Backend Issues

#### Import errors
**Problem**: `ModuleNotFoundError`
**Solution**: 
1. Ensure virtual environment is activated
2. Run from `api/` directory
3. Reinstall dependencies: `pip install -r requirements.txt`

#### Port 8000 in use
**Problem**: `Address already in use`
**Solution**:
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
# Or use different port
uvicorn app.main:app --port 8001
```

#### API key errors
**Problem**: `GOOGLE_API_KEY not set`
**Solution**:
1. Copy `.env.example` to `.env`
2. Add your API key from https://makersuite.google.com/app/apikey
3. Restart server

### Frontend Issues

#### npm install fails
**Problem**: Installation errors
**Solution**:
```bash
# Clear cache
npm cache clean --force
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Port 5173 in use
**Problem**: Port conflict
**Solution**: Vite automatically uses next available port

#### API connection errors
**Problem**: Cannot connect to backend
**Solution**:
1. Verify backend is running
2. Check `VITE_API_URL` in `.env`
3. Check CORS settings in backend

### Docker Issues

#### Build fails
**Problem**: Docker build errors
**Solution**:
```bash
# Clear Docker cache
docker-compose build --no-cache
```

#### Volume mount issues (Mac/Windows)
**Problem**: Files not syncing
**Solution**:
1. Check Docker Desktop file sharing settings
2. Add project directory to shared folders

#### Permission denied
**Problem**: Volume mount permission errors
**Solution**: Check file permissions, adjust as needed

## Getting Help

1. Check documentation in `plans/` directory
2. Search existing issues
3. Open a new issue with:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details
```

## 6. Testing Strategy

### Manual Testing

**Steps**:
1. Follow README setup instructions
2. Verify all commands work
3. Test on different OS if possible
4. Have another developer try setup

**Expected Results**:
- All instructions work step-by-step
- No missing steps
- Clear error messages documented

## 7. Checklist

### Implementation
- [ ] Create root README.md
- [ ] Create api/README.md
- [ ] Create web/README.md
- [ ] Create CONTRIBUTING.md
- [ ] Create docs/troubleshooting.md
- [ ] Review all planning docs

### Quality
- [ ] Check all links work
- [ ] Verify code examples run
- [ ] Test setup instructions
- [ ] Check spelling/grammar

### Review
- [ ] Self-review all docs
- [ ] Have team member review
- [ ] Test with new developer

## 8. Resources & References

**Documentation**:
- [Write the Docs](https://www.writethedocs.org/)
- [Documentation Best Practices](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide)

**Tools**:
- Markdown - Documentation format
- Mermaid - Diagrams in Markdown

## 9. Common Issues & Solutions

**Issue 1**: Docs out of sync with code
- **Solution**: Update docs with every PR
- **Prevention**: Add doc review to PR checklist

**Issue 2**: Too technical for beginners
- **Solution**: Add beginner-friendly sections
- **Prevention**: Test with new team members

## 10. Time Tracking

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Create READMEs | 1 hr | | |
| Create CONTRIBUTING | 30 min | | |
| Create troubleshooting | 30 min | | |
| Review all docs | 1 hr | | |
| **Total** | **3 hrs** | | |

## 11. Notes

**Documentation Principles**:
- Clear and concise
- Action-oriented
- Up-to-date
- Beginner-friendly

**Future Enhancements**:
- Add video tutorials
- Add interactive examples
- Add FAQ section
- Add architecture diagrams

---

**Task Status**: 🔴 Not Started
**Last Updated**: 2024-02-27
**Reviewer**: [Name]
