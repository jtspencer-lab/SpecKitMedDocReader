# Backend: Document Extraction & Analysis System

Production-ready Python/FastAPI backend for automated document processing with OCR, NLP, and human review.

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (recommended)

### Development Setup

1. **Clone repository**
```bash
git clone <repo-url>
cd SignUpReader
```

2. **Create Python virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd backend
pip install -e ".[dev]"
python -m spacy download en_core_web_md
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Initialize database**
```bash
alembic upgrade head
```

6. **Run development server**
```bash
uvicorn src.main:app --reload
```

API will be available at `http://localhost:8000`

### Using Docker Compose

```bash
docker-compose up --build
```

This starts:
- PostgreSQL (localhost:5432)
- Redis (localhost:6379)
- FastAPI (localhost:8000)
- Celery worker
- React frontend (localhost:5173)
- pgAdmin (localhost:5050)

## Project Structure

```
backend/
├── src/
│   ├── models/         # SQLAlchemy & Pydantic models
│   ├── services/       # Business logic
│   ├── api/            # FastAPI routes
│   ├── db/             # Database config
│   ├── tasks/          # Celery tasks
│   ├── utils/          # Utilities
│   └── main.py         # App entry point
├── tests/              # Test suite
├── migrations/         # Alembic migrations
├── pyproject.toml      # Dependencies
└── Dockerfile          # Production image
```

## Testing

Run unit/integration tests:
```bash
pytest --cov=src --cov-report=html
```

Target: >80% code coverage

## Database Migrations

Create migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Configuration

See `.env.example` for all available settings. Key settings:

- `DATABASE_URL`: PostgreSQL connection
- `REDIS_URL`: Redis connection
- `AZURE_FORM_RECOGNIZER_*`: OCR service credentials
- `SECRET_KEY`: JWT signing key (change in production!)
- `LOG_LEVEL`: Logging verbosity

## API Documentation

Auto-generated Swagger UI available at `http://localhost:8000/docs`

## Development Guidelines

- Use type hints for all functions
- Write tests before implementation (TDD)
- Follow PEP 8 style guide (enforced by Black)
- Document complex functions with docstrings
- Log important events using structlog

## Support

See `../README.md` for full project documentation.
