# Task 05: Environment Configuration

**Task ID**: sprint-0-t05
**Task Name**: Environment Configuration
**Sprint**: 0
**Priority**: High
**Estimated Time**: 2 hours
**Assigned To**: [Backend/Frontend Developer]

---

## 1. Objective

Create comprehensive environment configuration system for both backend and frontend, including .env files, validation, and documentation.

## 2. Why This Matters

### Business Value
- **Security**: API keys never committed to version control
- **Flexibility**: Easy to configure for different environments
- **Onboarding**: New developers can quickly set up their environment

### Technical Value
- **Configuration Management**: Centralized configuration
- **Validation**: Catch configuration errors at startup
- **Documentation**: Clear requirements for all variables

### Risks of Not Doing This
- **Security Breach**: API keys exposed in git history
- **Configuration Drift**: Different settings across environments
- **Debugging Nightmares**: Unclear which values are being used

## 3. Dependencies

### Prerequisites
- [x] t01-init-repo (repository structure exists)
- [x] t02-setup-python (backend config.py ready)
- [x] t03-setup-frontend (frontend ready)
- [x] t04-docker-config (Docker setup complete)

### Blocking
- [ ] Sprint 1 backend tasks (need API keys)
- [ ] Sprint 3 Gemini integration (need Gemini API key)

### External Dependencies
- None (configuration files only)

## 4. Acceptance Criteria

### Definition of Done
- [ ] Backend .env.example created with all variables
- [ ] Frontend .env.example created with all variables
- [ ] Root .env.example created for Docker Compose
- [ ] Environment variable documentation complete
- [ ] Backend validates required variables at startup
- [ ] Frontend validates required variables at startup
- [ ] Missing variables cause clear error messages
- [ ] .env files added to .gitignore

### Success Metrics
- All required variables documented
- Clear error messages for missing variables
- No sensitive data in .env.example files
- Easy setup process documented

### Edge Cases to Handle
- Missing required variables
- Invalid variable values
- Extra whitespace in values
- Comments in .env files

## 5. Technical Implementation

### Approach

1. Create backend .env.example
2. Create frontend .env.example
3. Create root .env.example for Docker
4. Implement backend validation
5. Implement frontend validation
6. Document all variables
7. Test missing variable handling

### Implementation Files

**api/.env.example**
```env
# =============================================================================
# AI Lightroom Backend Configuration
# =============================================================================
# Copy this file to .env and fill in your values
# NEVER commit .env to version control

# -----------------------------------------------------------------------------
# API Configuration
# -----------------------------------------------------------------------------
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# -----------------------------------------------------------------------------
# Gemini API Configuration
# -----------------------------------------------------------------------------
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_api_key_here
GOOGLE_MODEL=gemini-1.5-pro-vision
GOOGLE_MODEL_TEXT=gemini-1.5-pro

# -----------------------------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------------------------
# Comma-separated list of allowed origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# -----------------------------------------------------------------------------
# File Upload Configuration
# -----------------------------------------------------------------------------
# Maximum file size in bytes (default: 10MB)
MAX_UPLOAD_SIZE=10485760
# Comma-separated list of allowed file extensions
ALLOWED_EXTENSIONS=jpg,jpeg,png,webp

# -----------------------------------------------------------------------------
# Logging Configuration
# -----------------------------------------------------------------------------
LOG_LEVEL=INFO
LOG_FORMAT=json

# -----------------------------------------------------------------------------
# Rate Limiting (Future)
# -----------------------------------------------------------------------------
RATE_LIMIT_PER_MINUTE=60

# -----------------------------------------------------------------------------
# Optional: Production Settings
# -----------------------------------------------------------------------------
# Uncomment for production
# DEBUG=false
# LOG_LEVEL=WARNING
```

**api/app/config.py** (enhanced)
```python
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache
import sys


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Gemini API
    GOOGLE_API_KEY: str = ""
    GOOGLE_MODEL: str = "gemini-1.5-pro-vision"
    GOOGLE_MODEL_TEXT: str = "gemini-1.5-pro"
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: str = "jpg,jpeg,png,webp"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Rate Limiting (future)
    RATE_LIMIT_PER_MINUTE: int = 60
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Parse allowed extensions from comma-separated string"""
        return [ext.strip().lower() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    def validate_required(self) -> None:
        """Validate required settings"""
        errors = []
        
        if not self.GOOGLE_API_KEY or self.GOOGLE_API_KEY == "your_gemini_api_key_here":
            errors.append("GOOGLE_API_KEY is required. Get your key from https://makersuite.google.com/app/apikey")
        
        if self.API_PORT < 1 or self.API_PORT > 65535:
            errors.append(f"Invalid API_PORT: {self.API_PORT}")
        
        if self.MAX_UPLOAD_SIZE < 1:
            errors.append("MAX_UPLOAD_SIZE must be positive")
        
        if errors:
            print("\n❌ Configuration Errors:\n")
            for error in errors:
                print(f"  • {error}")
            print("\nPlease check your .env file and try again.\n")
            sys.exit(1)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    settings.validate_required()
    return settings


# Global settings instance
settings = get_settings()
```

**web/.env.example**
```env
# =============================================================================
# AI Lightroom Frontend Configuration
# =============================================================================
# Copy this file to .env and fill in your values
# NEVER commit .env to version control

# -----------------------------------------------------------------------------
# API Configuration
# -----------------------------------------------------------------------------
# Backend API URL (change for production)
VITE_API_URL=http://localhost:8000

# API request timeout in milliseconds
VITE_API_TIMEOUT=30000

# -----------------------------------------------------------------------------
# File Upload Configuration
# -----------------------------------------------------------------------------
# Maximum file size in bytes (should match backend)
VITE_MAX_FILE_SIZE=10485760

# -----------------------------------------------------------------------------
# Feature Flags (Future)
# -----------------------------------------------------------------------------
# VITE_ENABLE_BATCH_PROCESSING=false
# VITE_ENABLE_USER_ACCOUNTS=false
```

**web/src/config.js**
```javascript
/**
 * Frontend configuration with validation
 */

const requiredEnvVars = [
  'VITE_API_URL',
];

const config = {
  // API Configuration
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  apiTimeout: Number(import.meta.env.VITE_API_TIMEOUT) || 30000,
  
  // File Upload
  maxFileSize: Number(import.meta.env.VITE_MAX_FILE_SIZE) || 10485760, // 10MB
  
  // Feature Flags
  enableBatchProcessing: import.meta.env.VITE_ENABLE_BATCH_PROCESSING === 'true',
  enableUserAccounts: import.meta.env.VITE_ENABLE_USER_ACCOUNTS === 'true',
  
  // Environment
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,
};

/**
 * Validate required environment variables
 */
export function validateConfig() {
  const errors = [];
  
  for (const envVar of requiredEnvVars) {
    if (!import.meta.env[envVar]) {
      errors.push(`Missing required environment variable: ${envVar}`);
    }
  }
  
  if (config.maxFileSize < 1) {
    errors.push('VITE_MAX_FILE_SIZE must be positive');
  }
  
  if (config.apiTimeout < 1000) {
    errors.push('VITE_API_TIMEOUT should be at least 1000ms');
  }
  
  if (errors.length > 0) {
    console.error('\n❌ Configuration Errors:\n');
    errors.forEach(error => console.error(`  • ${error}`));
    console.error('\nPlease check your .env file and try again.\n');
    throw new Error('Invalid configuration');
  }
  
  return config;
}

export default config;
```

**.env.example** (root, for Docker Compose)
```env
# =============================================================================
# AI Lightroom Docker Compose Configuration
# =============================================================================
# Copy this file to .env and fill in your values
# NEVER commit .env to version control

# -----------------------------------------------------------------------------
# Gemini API Key (Required)
# -----------------------------------------------------------------------------
# Get your API key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your_gemini_api_key_here

# -----------------------------------------------------------------------------
# Docker Configuration
# -----------------------------------------------------------------------------
# These values are used by docker-compose.yml
COMPOSE_PROJECT_NAME=ai-lightroom
```

**docs/environment-variables.md**
```markdown
# Environment Variables Documentation

## Backend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_HOST` | No | `0.0.0.0` | Host address for API server |
| `API_PORT` | No | `8000` | Port for API server |
| `DEBUG` | No | `true` | Enable debug mode |
| `GOOGLE_API_KEY` | **Yes** | - | Gemini API key for AI features |
| `GOOGLE_MODEL` | No | `gemini-1.5-pro-vision` | Vision model for image analysis |
| `GOOGLE_MODEL_TEXT` | No | `gemini-1.5-pro` | Text model for preset generation |
| `CORS_ORIGINS` | No | `http://localhost:5173` | Comma-separated allowed origins |
| `MAX_UPLOAD_SIZE` | No | `10485760` | Max file size in bytes (10MB) |
| `ALLOWED_EXTENSIONS` | No | `jpg,jpeg,png,webp` | Allowed file extensions |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `LOG_FORMAT` | No | `json` | Log format (json or text) |

## Frontend Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_URL` | **Yes** | - | Backend API URL |
| `VITE_API_TIMEOUT` | No | `30000` | API timeout in milliseconds |
| `VITE_MAX_FILE_SIZE` | No | `10485760` | Max file size in bytes |

## Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

## Security Best Practices

- **Never commit .env files** to version control
- **Use different keys** for development and production
- **Rotate keys** periodically
- **Restrict key usage** in Google Cloud Console if possible
```

### Pseudocode / Algorithm

```bash
# Step 1: Create .env.example files
# Create api/.env.example
# Create web/.env.example
# Create .env.example (root)

# Step 2: Copy to .env files
cp api/.env.example api/.env
cp web/.env.example web/.env
cp .env.example .env

# Step 3: Fill in your values
# Edit each .env file with your actual values

# Step 4: Verify .env is in .gitignore
grep -q ".env" .gitignore || echo ".env" >> .gitignore

# Step 5: Test configuration loading
cd api && python -c "from app.config import settings; print(settings)"
cd web && npm run dev  # Check console for errors
```

## 6. Testing Strategy

### Manual Testing

**Steps**:
1. Copy all .env.example to .env
2. Leave GOOGLE_API_KEY empty
3. Try to start backend - should show clear error
4. Fill in GOOGLE_API_KEY
5. Start backend - should work
6. Test same for frontend

**Expected Results**:
- Missing required variables show clear error
- Valid configuration loads successfully
- No sensitive data in example files

## 7. Checklist

### Implementation
- [ ] Create api/.env.example
- [ ] Create web/.env.example
- [ ] Create root .env.example
- [ ] Implement backend config validation
- [ ] Implement frontend config validation
- [ ] Create environment variables documentation
- [ ] Add .env to .gitignore (verify)

### Testing
- [ ] Test missing variable handling
- [ ] Test invalid value handling
- [ ] Test successful configuration load
- [ ] Test with Docker Compose

### Documentation
- [ ] Document all variables
- [ ] Add getting started guide
- [ ] Add security best practices

### Review
- [ ] Verify no sensitive data in examples
- [ ] Check validation is comprehensive
- [ ] Review error messages for clarity

## 8. Resources & References

**Documentation**:
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [Vite Environment Variables](https://vitejs.dev/guide/env-and-mode.html)
- [12-Factor App Config](https://12factor.net/config)

**Best Practices**:
- [Environment Variables Best Practices](https://developer.squareup.com/blog/environment-variables-considered-harmful/)
- [Secrets Management](https://www.hashicorp.com/blog/managing-secrets-with-vault-and-consul)

## 9. Common Issues & Solutions

**Issue 1**: .env file not loading
- **Solution**: Check file is in correct directory, no syntax errors
- **Prevention**: Use .env.example as template

**Issue 2**: Variables with spaces not working
- **Solution**: Don't quote values in .env, or use proper quoting
- **Prevention**: Document proper format

**Issue 3**: Changes not reflecting
- **Solution**: Restart server after changing .env
- **Prevention**: Document that restart is required

**Issue 4**: API key exposed in git
- **Solution**: Rotate key immediately, remove from git history
- **Prevention**: Verify .gitignore before committing

## 10. Time Tracking

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Create .env.example files | 30 min | | |
| Implement validation | 45 min | | |
| Create documentation | 30 min | | |
| Test everything | 30 min | | |
| **Total** | **2.5 hrs** | | |

## 11. Notes

**Configuration Priority**:
1. Environment variables (highest)
2. .env file
3. Default values (lowest)

**Future Enhancements**:
- Add configuration validation schema
- Add secrets management integration
- Add environment-specific config files
- Add configuration UI for admins

---

**Task Status**: 🔴 Not Started
**Last Updated**: 2024-02-27
**Reviewer**: [Name]
