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
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
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
- [Sprint 0 Walkthrough](./SPRINT_0_WALKTHROUGH.md)

## License

MIT License - see [LICENSE](./LICENSE)
