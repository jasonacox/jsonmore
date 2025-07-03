# GitHub Actions CI/CD

This repository includes comprehensive GitHub Actions workflows for continuous integration and deployment.

## Workflows

### 🔄 CI (`.github/workflows/ci.yml`)
**Comprehensive testing and quality checks**
- **Triggers**: Push to `main`/`develop`, Pull Requests to `main`
- **Test Matrix**: Python 3.8-3.12 on Ubuntu, Windows, macOS
- **Features**:
  - Run legacy tests (`python test_jsonmore.py`)
  - Run comprehensive unittest suite (`python test_jsonmore.py --comprehensive`) 
  - Run pytest with coverage (`pytest --cov=jsonmore`)
  - Code formatting check with `black`
  - Linting with `flake8`
  - Type checking with `mypy`
  - Package building and installation testing
  - Coverage reporting to Codecov

### ⚡ Simple Tests (`.github/workflows/test-simple.yml`)
**Lightweight testing workflow**
- **Triggers**: Push/PR to `main`
- **Test Matrix**: Python 3.8-3.12 on Ubuntu only
- **Features**:
  - Quick pytest execution
  - Legacy test validation

### 🚀 PyPI Publish (`.github/workflows/publish.yml`)
**Automatic package publishing**
- **Triggers**: GitHub Release creation
- **Features**:
  - Build package with `python -m build`
  - Validate package with `twine check`
  - Publish to PyPI using API token

## Setup Requirements

### 1. Repository Secrets
For the publish workflow, add these secrets in GitHub:
- `PYPI_API_TOKEN`: Your PyPI API token

### 2. Coverage Reporting (Optional)
For Codecov integration:
- Sign up at [codecov.io](https://codecov.io)
- Link your repository
- Coverage reports will be automatically uploaded

## Local Testing

Before pushing, you can run the same checks locally:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jsonmore --cov-report=term-missing

# Check code formatting
black --check jsonmore/ test_jsonmore.py

# Run linting
flake8 jsonmore/ test_jsonmore.py

# Type checking
mypy jsonmore/ --ignore-missing-imports

# Build package
python -m build
```

## Badge Integration

Add these badges to your README.md:

```markdown
[![CI](https://github.com/jasonacox/jsonmore/workflows/CI/badge.svg)](https://github.com/jasonacox/jsonmore/actions/workflows/ci.yml)
[![Tests](https://github.com/jasonacox/jsonmore/workflows/Tests/badge.svg)](https://github.com/jasonacox/jsonmore/actions/workflows/test-simple.yml)
[![PyPI](https://img.shields.io/pypi/v/jsonmore)](https://pypi.org/project/jsonmore/)
[![Python](https://img.shields.io/pypi/pyversions/jsonmore)](https://pypi.org/project/jsonmore/)
[![codecov](https://codecov.io/gh/jasonacox/jsonmore/branch/main/graph/badge.svg)](https://codecov.io/gh/jasonacox/jsonmore)
```
