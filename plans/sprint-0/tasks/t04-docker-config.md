# Task 04: Docker Configuration

**Task ID**: sprint-0-t04
**Task Name**: Docker Configuration
**Sprint**: 0
**Priority**: Medium
**Estimated Time**: 2 hours
**Assigned To**: [DevOps Developer]

---

## 1. Objective

Create Docker configuration for both backend and frontend services with multi-stage builds, enabling consistent development and production environments.

## 2. Why This Matters

### Business Value
- **Consistency**: Eliminates "works on my machine" problems
- **Onboarding**: New developers can start in minutes
- **Production Ready**: Same containers used in development and production

### Technical Value
- **Isolation**: Each service runs in its own container
- **Scalability**: Easy to scale services independently
- **Reproducibility**: Identical environments across all machines

### Risks of Not Doing This
- **Environment Drift**: Different configurations across machines
- **Deployment Issues**: Development works but production fails
- **Slow Onboarding**: New developers spend hours on setup

## 3. Dependencies

### Prerequisites
- [x] t01-init-repo (repository structure exists)
- [x] t02-setup-python (backend structure ready)
- [x] t03-setup-frontend (frontend structure ready)
- [x] Docker Desktop installed and running

### Blocking
- [ ] Sprint 7 deployment tasks (builds on this)
- [ ] Production deployment

### External Dependencies
- Docker Engine 24.0+
- Docker Compose 2.21+

## 4. Acceptance Criteria

### Definition of Done
- [ ] Backend Dockerfile created with multi-stage build
- [ ] Frontend Dockerfile created with multi-stage build
- [ ] docker-compose.yml configured for development
- [ ] Volume mounts working for hot reload
- [ ] Network configuration for inter-container communication
- [ ] Environment variables configured
- [ ] Health checks configured
- [ ] Both containers start successfully
- [ ] Frontend can call backend API

### Success Metrics
- Backend container builds in < 2 minutes
- Frontend container builds in < 2 minutes
- docker-compose up starts both services
- Code changes hot reload in containers
- API calls work between containers

### Edge Cases to Handle
- Docker not running
- Port conflicts (8000, 5173)
- Volume mount permission issues
- Build cache issues

## 5. Technical Implementation

### Approach

1. Create backend Dockerfile with multi-stage build
2. Create frontend Dockerfile with multi-stage build
3. Create docker-compose.yml for development
4. Configure volume mounts for hot reload
5. Configure networking
6. Add health checks
7. Test complete setup

### Implementation Files

**api/Dockerfile**
```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir uv && \
    uv pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**api/Dockerfile.dev**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir uv && \
    uv pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Run application with reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**web/Dockerfile**
```dockerfile
# Build stage
FROM node:20-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine as production

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

**web/Dockerfile.dev**
```dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Expose port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev", "--", "--host"]
```

**web/nginx.conf**
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

**docker-compose.yml**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./api
      dockerfile: Dockerfile.dev
    container_name: ai-lightroom-backend
    ports:
      - "8000:8000"
    volumes:
      - ./api:/app
      - /app/.venv
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DEBUG=true
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
      - CORS_ORIGINS=http://localhost:5173,http://localhost:3000
    env_file:
      - ./api/.env
    networks:
      - ai-lightroom-network
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./web
      dockerfile: Dockerfile.dev
    container_name: ai-lightroom-frontend
    ports:
      - "5173:5173"
    volumes:
      - ./web:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_API_TIMEOUT=30000
    env_file:
      - ./web/.env
    networks:
      - ai-lightroom-network
    depends_on:
      backend:
        condition: service_healthy

networks:
  ai-lightroom-network:
    driver: bridge

volumes:
  node_modules:
```

**docker-compose.prod.yml**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./api
      dockerfile: Dockerfile
      target: production
    container_name: ai-lightroom-backend-prod
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
      - DEBUG=false
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    env_file:
      - ./api/.env
    networks:
      - ai-lightroom-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  frontend:
    build:
      context: ./web
      dockerfile: Dockerfile
      target: production
    container_name: ai-lightroom-frontend-prod
    ports:
      - "80:80"
    networks:
      - ai-lightroom-network
    depends_on:
      - backend
    restart: unless-stopped

networks:
  ai-lightroom-network:
    driver: bridge
```

**.dockerignore (root)**
```
node_modules
.git
.gitignore
*.md
.env
.env.*
.venv
venv
__pycache__
*.pyc
.pytest_cache
.coverage
htmlcov
dist
build
.DS_Store
*.log
```

### Pseudocode / Algorithm

```bash
# Step 1: Create Dockerfiles
# Create api/Dockerfile, api/Dockerfile.dev
# Create web/Dockerfile, web/Dockerfile.dev

# Step 2: Create docker-compose files
# Create docker-compose.yml (development)
# Create docker-compose.prod.yml (production)

# Step 3: Create .dockerignore
# Exclude unnecessary files from build context

# Step 4: Build and test
docker-compose build
docker-compose up

# Step 5: Verify
# Open http://localhost:5173
# Open http://localhost:8000/docs
# Test API call from frontend

# Step 6: Cleanup
docker-compose down
```

## 6. Testing Strategy

### Manual Testing

**Steps**:
1. Run `docker-compose build`
2. Run `docker-compose up`
3. Open http://localhost:5173 - should see frontend
4. Open http://localhost:8000/docs - should see API docs
5. Modify backend code - should auto-reload
6. Modify frontend code - should hot reload
7. Run `docker-compose down`

**Expected Results**:
- Both containers build successfully
- Both services start without errors
- Hot reload works in both containers
- Frontend can call backend API

### Integration Testing

**Scenarios**:
- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] API call from frontend to backend works
- [ ] Environment variables loaded correctly

## 7. Checklist

### Implementation
- [ ] Create backend Dockerfile
- [ ] Create backend Dockerfile.dev
- [ ] Create frontend Dockerfile
- [ ] Create frontend Dockerfile.dev
- [ ] Create docker-compose.yml
- [ ] Create docker-compose.prod.yml
- [ ] Create nginx.conf
- [ ] Create .dockerignore files
- [ ] Configure volume mounts
- [ ] Configure networking
- [ ] Add health checks

### Testing
- [ ] Test backend container build
- [ ] Test frontend container build
- [ ] Test docker-compose up
- [ ] Test hot reload in containers
- [ ] Test inter-container communication
- [ ] Test docker-compose down

### Documentation
- [ ] Document Docker commands
- [ ] Document environment setup
- [ ] Add troubleshooting guide

### Review
- [ ] Self-review Dockerfiles
- [ ] Verify security best practices
- [ ] Check build optimization

## 8. Resources & References

**Documentation**:
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)

**Tools**:
- Docker - Containerization platform
- Docker Compose - Multi-container orchestration

**Best Practices**:
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Security Best Practices](https://snyk.io/blog/10-docker-image-security-best-practices/)

## 9. Common Issues & Solutions

**Issue 1**: Volume mounts not working
- **Solution**: Check Docker Desktop file sharing settings
- **Prevention**: Document required shared directories

**Issue 2**: Port already in use
- **Solution**: Change ports in docker-compose.yml or stop conflicting services
- **Prevention**: Document port usage

**Issue 3**: Build fails due to cache
- **Solution**: Run `docker-compose build --no-cache`
- **Prevention**: Regular cache cleanup

**Issue 4**: Permission denied on volumes
- **Solution**: Adjust file permissions or Docker settings
- **Prevention**: Use consistent user mapping

## 10. Time Tracking

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Create backend Dockerfile | 30 min | | |
| Create frontend Dockerfile | 30 min | | |
| Create docker-compose | 30 min | | |
| Configure volumes/networks | 15 min | | |
| Test everything | 30 min | | |
| **Total** | **2.5 hrs** | | |

## 11. Notes

**Development Workflow**:

1. Run `docker-compose up` to start development environment
2. Make code changes - containers auto-reload
3. Run `docker-compose down` to stop

**Production Deployment**:

1. Run `docker-compose -f docker-compose.prod.yml up -d`
2. Containers run in production mode
3. Use proper environment variables

**Future Enhancements**:
- Add Redis container for caching
- Add PostgreSQL container for data
- Add monitoring with Prometheus
- Add CI/CD pipeline integration

---

**Task Status**: 🔴 Not Started
**Last Updated**: 2024-02-27
**Reviewer**: [Name]
