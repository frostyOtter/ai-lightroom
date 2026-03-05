# Task 06: Git Setup and Workflow

**Task ID**: sprint-0-t06
**Task Name**: Git Setup and Workflow
**Sprint**: 0
**Priority**: Medium
**Estimated Time**: 1 hour
**Assigned To**: [Developer]

---

## 1. Objective

Configure Git with hooks, code formatters, linters, and commit message guidelines to ensure consistent code quality across the team.

## 2. Why This Matters

### Business Value
- **Code Consistency**: All code follows same style
- **Quality Assurance**: Automated checks catch issues early
- **Professionalism**: Clean git history and commit messages

### Technical Value
- **Automated Quality**: No manual style reviews needed
- **Early Bug Detection**: Linting catches errors before commit
- **Clean History**: Meaningful commit messages

### Risks of Not Doing This
- **Inconsistent Code**: Different styles across codebase
- **Review Overhead**: Reviewers focus on style, not logic
- **Merge Conflicts**: Formatting changes cause conflicts

## 3. Dependencies

### Prerequisites
- [x] t01-init-repo (repository initialized)
- [x] t02-setup-python (Python tools available)
- [x] t03-setup-frontend (Node tools available)

### Blocking
- [ ] All future commits (benefit from setup)

### External Dependencies
- Git hooks (pre-commit)
- Python formatters (black, ruff, mypy)
- Node linters (eslint, prettier)

## 4. Acceptance Criteria

### Definition of Done
- [ ] .gitattributes configured
- [ ] Pre-commit hooks configured
- [ ] Python formatter configured (black)
- [ ] Python linter configured (ruff)
- [ ] Python type checker configured (mypy)
- [ ] JavaScript linter configured (eslint)
- [ ] JavaScript formatter configured (prettier)
- [ ] Commit message guidelines documented
- [ ] Branch naming conventions documented
- [ ] Hooks tested and working

### Success Metrics
- All hooks run on commit
- Code automatically formatted
- Linting errors caught
- Commit messages follow guidelines

### Edge Cases to Handle
- Hooks failing on valid code
- Performance issues with hooks
- Developer bypassing hooks

## 5. Technical Implementation

### Approach

1. Configure .gitattributes
2. Set up pre-commit framework
3. Configure Python tools
4. Configure JavaScript tools
5. Document conventions
6. Test hooks

### Implementation Files

**.gitattributes**
```
# Auto detect text files and perform LF normalization
* text=auto

# Source code
*.py text eol=lf
*.js text eol=lf
*.jsx text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.json text eol=lf
*.yaml text eol=lf
*.yml text eol=lf
*.md text eol=lf
*.txt text eol=lf

# Config files
.env* text eol=lf
.gitignore text eol=lf
.gitattributes text eol=lf
Dockerfile text eol=lf
docker-compose*.yml text eol=lf

# Shell scripts
*.sh text eol=lf

# Binary files
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
```

**.pre-commit-config.yaml**
```yaml
# Pre-commit hooks configuration
# Install: uv pip install pre-commit && pre-commit install

repos:
  # Python hooks
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11
        files: ^api/

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
        files: ^api/

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.5.0
          - types-requests
        files: ^api/

  # JavaScript/TypeScript hooks
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.55.0
    hooks:
      - id: eslint
        files: ^web/
        types: [file]
        args: [--fix]
        additional_dependencies:
          - eslint@8.55.0
          - eslint-plugin-react@7.33.0
          - eslint-plugin-react-hooks@4.6.0

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        files: ^web/
        types_or: [javascript, jsx, ts, tsx, json, css]

  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
        args: [--unsafe]
      - id: check-json
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: check-merge-conflict
      - id: detect-private-key
      - id: no-commit-to-branch
        args: [--branch, main, --branch, master]

  # Commit message
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

**api/pyproject.toml**
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

[tool.ruff]
line-length = 88
target-version = "py311"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by black)
    "B008",  # do not perform function calls in argument defaults
]

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = ["cv2.*", "PIL.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --cov=app --cov-report=term-missing"
```

**web/.eslintrc.cjs**
```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parserOptions: { ecmaVersion: 'latest', sourceType: 'module' },
  settings: { react: { version: '18.2' } },
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    'react/prop-types': 'off',
  },
}
```

**web/.prettierrc**
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "jsxSingleQuote": false,
  "bracketSpacing": true,
  "bracketSameLine": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

**docs/git-workflow.md**
```markdown
# Git Workflow and Conventions

## Branch Naming

Use the following prefixes:
- `feature/` - New features (e.g., `feature/image-upload`)
- `bugfix/` - Bug fixes (e.g., `bugfix/fix-upload-error`)
- `hotfix/` - Emergency production fixes (e.g., `hotfix/api-crash`)
- `refactor/` - Code refactoring (e.g., `refactor/api-structure`)
- `docs/` - Documentation updates (e.g., `docs/api-guide`)
- `test/` - Test additions/updates (e.g., `test/unit-tests`)

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```
feat(api): add image analysis endpoint

- Add histogram extraction
- Add luminance calculation
- Add color detection

Closes #123
```

```
fix(frontend): handle image upload errors

Fix error handling for large file uploads.
Display user-friendly error messages.

Fixes #456
```

## Workflow

1. Create branch from `develop`
2. Make changes following code style
3. Commit with conventional message
4. Push and create PR
5. Wait for CI and review
6. Squash and merge

## Pre-commit Hooks

Hooks run automatically on commit:
- Code formatting (black, prettier)
- Linting (ruff, eslint)
- Type checking (mypy)
- File checks (trailing whitespace, etc.)

Bypass if needed: `git commit --no-verify` (use sparingly)
```

### Pseudocode / Algorithm

```bash
# Step 1: Install pre-commit
uv pip install pre-commit

# Step 2: Create configuration files
# Create .pre-commit-config.yaml
# Create pyproject.toml
# Create .eslintrc.cjs
# Create .prettierrc

# Step 3: Install hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Step 4: Run on all files (optional)
pre-commit run --all-files

# Step 5: Test hooks
# Make a commit - hooks should run automatically
```

## 6. Testing Strategy

### Manual Testing

**Steps**:
1. Install pre-commit hooks
2. Make code change with style violation
3. Attempt commit - should fail
4. Fix violation
5. Commit again - should pass

**Expected Results**:
- Hooks catch style violations
- Code is auto-formatted
- Linting errors are shown

## 7. Checklist

### Implementation
- [ ] Create .gitattributes
- [ ] Create .pre-commit-config.yaml
- [ ] Create api/pyproject.toml
- [ ] Create web/.eslintrc.cjs
- [ ] Create web/.prettierrc
- [ ] Install pre-commit hooks
- [ ] Document workflow

### Testing
- [ ] Test Python formatting
- [ ] Test Python linting
- [ ] Test JavaScript linting
- [ ] Test JavaScript formatting
- [ ] Test commit message format

### Documentation
- [ ] Document branch naming
- [ ] Document commit format
- [ ] Document workflow

## 8. Resources & References

**Documentation**:
- [Pre-commit](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Black](https://black.readthedocs.io/)
- [Ruff](https://docs.astral.sh/ruff/)
- [ESLint](https://eslint.org/)

**Tools**:
- pre-commit - Git hook framework
- black - Python formatter
- ruff - Python linter
- eslint - JavaScript linter
- prettier - JavaScript formatter

## 9. Common Issues & Solutions

**Issue 1**: Hooks too slow
- **Solution**: Use `SKIP=hook-id git commit` for specific hooks
- **Prevention**: Keep hooks minimal, run full suite in CI

**Issue 2**: Hook conflicts with editor
- **Solution**: Configure editor to use same formatter settings
- **Prevention**: Share editor config

**Issue 3**: Cannot commit due to hooks
- **Solution**: Fix the issues, or use `--no-verify` temporarily
- **Prevention**: Run hooks manually before committing

## 10. Time Tracking

| Activity | Estimated | Actual | Notes |
|----------|-----------|--------|-------|
| Create config files | 20 min | | |
| Install and test hooks | 20 min | | |
| Document conventions | 20 min | | |
| **Total** | **1 hr** | | |

## 11. Notes

**Performance Tips**:
- Hooks run only on changed files by default
- Use `pre-commit run --all-files` for full scan
- CI should run full suite on all files

**Future Enhancements**:
- Add commitlint for message format
- Add secret detection
- Add spell checking
- Add CI/CD integration

---

**Task Status**: 🔴 Not Started
**Last Updated**: 2024-02-27
**Reviewer**: [Name]
