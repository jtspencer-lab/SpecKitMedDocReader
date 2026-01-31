# Backend Tests

This directory contains the test suite for the Document Extraction & Analysis backend.

## Structure

- `unit/`: Unit tests for individual components (models, services, utilities)
- `integration/`: Integration tests (API endpoints, database interactions)
- `conftest.py`: Pytest configuration and shared fixtures

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/unit/test_models.py
```

Run tests matching pattern:
```bash
pytest -k "test_document"
```

## Coverage Target

Minimum 80% code coverage required. Coverage report is generated in `htmlcov/index.html`.

## Test Patterns

- Use `@pytest.mark.asyncio` for async tests
- Use fixtures for database setup (see `conftest.py`)
- Mock external services (Azure Form Recognizer, etc.)
- Test both success and error cases
