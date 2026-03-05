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
   Follow conventional commit format:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Adding/updating tests
   - `chore:` - Maintenance tasks

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
- Use functional components with hooks
- Follow existing patterns

## Testing

- Write unit tests for all new features
- Maintain test coverage above 80%
- Run tests before committing

## Documentation

- Update README.md if needed
- Update API docs for new endpoints
- Add docstrings for new functions

## Branch Naming

Use the following prefixes:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Emergency production fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions/updates

## Questions?

Open an issue or contact the maintainers.
