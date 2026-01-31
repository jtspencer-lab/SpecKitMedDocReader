# Quick Start Guide: Document Extraction & Analysis System

**Purpose**: Get the development environment running locally in under 30 minutes

---

## Prerequisites

Ensure your system has these installed:

- **Docker** (≥ 20.10) - [Install](https://docs.docker.com/get-docker/)
- **Docker Compose** (≥ 2.0) - [Install](https://docs.docker.com/compose/install/)
- **Git** (for cloning the repository)
- **Python 3.11+** (optional, for local debugging)
- **Node.js 18+** (optional, for frontend development)

**Verify Installation**:
```bash
docker --version    # Should be >= 20.10
docker-compose --version  # Should be >= 2.0
```

---

## Step 1: Clone and Setup (5 minutes)

```bash
# Clone the repository
git clone <repository-url>
cd SignUpReader

# Copy environment template
cp .env.example .env

# Review .env file (database passwords, API keys, etc)
# For development, defaults are fine
cat .env
```

**Key Environment Variables**:
```
# Database
POSTGRES_USER=signup_dev
POSTGRES_PASSWORD=dev_password
POSTGRES_DB=signup_extraction

# Backend
FASTAPI_ENV=development
FASTAPI_PORT=8000

# Frontend
REACT_PORT=3000

# Azure (optional for local development, required for production)
AZURE_FORM_RECOGNIZER_ENDPOINT=<your-azure-endpoint>
AZURE_FORM_RECOGNIZER_KEY=<your-azure-key>
```

---

## Step 2: Start Services (5 minutes)

```bash
# Start all services with Docker Compose
docker-compose up --build

# Expected output:
# postgres_1    | database system is ready to accept connections
# redis_1       | Ready to accept connections
# api_1         | Uvicorn running on http://0.0.0.0:8000
# frontend_1    | webpack compiled successfully
```

Services started:
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **FastAPI Backend**: http://localhost:8000
- **React Frontend**: http://localhost:3000
- **pgAdmin** (DB UI): http://localhost:5050

---

## Step 3: Initialize Database (2 minutes)

In another terminal:

```bash
# Run database migrations
docker-compose exec api alembic upgrade head

# Create test user (optional)
docker-compose exec api python -c "
from src.db import get_db
from src.models import User
db = next(get_db())
user = User(username='test@example.com', email='test@example.com')
db.add(user)
db.commit()
print('Test user created')
"
```

---

## Step 4: Access the Application (1 minute)

Open your browser:

1. **Frontend Dashboard**: http://localhost:3000
   - Upload documents
   - View extraction results
   - Review and approve extractions

2. **API Documentation**: http://localhost:8000/docs
   - Interactive Swagger UI
   - Try API endpoints directly
   - Download OpenAPI spec

3. **Database Admin**: http://localhost:5050
   - Username: admin@example.com
   - Password: admin

---

## Common Tasks

### Upload a Test Document

**Via Web UI**:
1. Go to http://localhost:3000
2. Click "Upload Document"
3. Select a PDF or image file
4. Click "Upload"
5. Wait for processing (will take 10-30 seconds)
6. Click "View Results" once processing completes

**Via API (curl)**:
```bash
curl -X POST http://localhost:8000/api/v1/documents \
  -H "Authorization: Bearer test-token" \
  -F "file=@document.pdf"

# Returns:
# {
#   "id": "550e8400-e29b-41d4-a716-446655440000",
#   "filename": "document.pdf",
#   "processing_status": "pending",
#   "upload_date": "2026-01-19T10:00:00Z"
# }
```

### Check Processing Status

```bash
curl http://localhost:8000/api/v1/documents/550e8400-e29b-41d4-a716-446655440000/status \
  -H "Authorization: Bearer test-token"

# Returns:
# {
#   "status": "processing",
#   "progress_percent": 45,
#   "estimated_time_seconds": 15
# }
```

### Retrieve Extraction Results

```bash
curl http://localhost:8000/api/v1/documents/550e8400-e29b-41d4-a716-446655440000/results \
  -H "Authorization: Bearer test-token"

# Returns extraction data with confidence scores
```

### View Logs

```bash
# API logs
docker-compose logs -f api

# Worker logs
docker-compose logs -f celery_worker

# All services
docker-compose logs -f
```

---

## Testing

### Run Unit Tests (Backend)

```bash
# Run all tests
docker-compose exec api pytest

# Run specific test file
docker-compose exec api pytest tests/unit/test_extraction_service.py

# Run with coverage
docker-compose exec api pytest --cov=src tests/
```

### Run Frontend Tests

```bash
# Run Jest tests
docker-compose exec frontend npm test

# Run with coverage
docker-compose exec frontend npm test -- --coverage
```

### Run End-to-End Tests

```bash
# Requires frontend and backend running
docker-compose exec frontend npm run test:e2e
```

---

## Development Workflow

### Making Backend Changes

1. Edit Python files in `backend/src/`
2. Changes auto-reload in development mode (FastAPI hot-reload enabled)
3. Check logs for any errors: `docker-compose logs -f api`

### Making Frontend Changes

1. Edit React files in `frontend/src/`
2. Changes auto-reload in browser (React dev server hot-reload)
3. Check browser console for any errors

### Database Schema Changes

1. Edit `backend/src/db/models.py`
2. Create a migration: `docker-compose exec api alembic revision --autogenerate -m "your change description"`
3. Review migration file in `backend/migrations/versions/`
4. Apply migration: `docker-compose exec api alembic upgrade head`

---

## Troubleshooting

### Services Won't Start

```bash
# Check if ports are in use
lsof -i :8000  # FastAPI
lsof -i :3000  # Frontend
lsof -i :5432  # PostgreSQL

# Kill processes on those ports (if needed)
kill -9 <PID>

# Try again
docker-compose down
docker-compose up --build
```

### Database Connection Error

```bash
# Wait for PostgreSQL to be ready
docker-compose logs postgres

# Check database credentials in .env file
# Restart database
docker-compose restart postgres

# Reinitialize
docker-compose exec api alembic upgrade head
```

### API Requests Return 401 Unauthorized

```bash
# Add Bearer token header (for development, any token works locally)
curl http://localhost:8000/api/v1/health \
  -H "Authorization: Bearer test-token"
```

### Out of Disk Space

```bash
# Docker containers can consume space
docker system prune -a
docker volume prune
```

---

## Project Structure Reference

```
backend/
├── src/
│   ├── api/              # FastAPI route handlers
│   ├── services/         # Business logic
│   ├── models/           # Pydantic & SQLAlchemy models
│   ├── db/               # Database configuration
│   ├── tasks/            # Celery async tasks
│   └── utils/            # Helpers & utilities
├── tests/
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
└── main.py               # FastAPI app entry point

frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/            # Page routes
│   ├── services/         # API client
│   └── types/            # TypeScript interfaces
└── tests/                # Jest tests

docker-compose.yml       # Local development stack
```

---

## Key API Endpoints for Testing

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | System health check |
| POST | `/api/v1/documents` | Upload document |
| GET | `/api/v1/documents` | List documents |
| GET | `/api/v1/documents/{id}/status` | Check status |
| GET | `/api/v1/documents/{id}/results` | Get extraction results |
| GET | `/api/v1/reviews` | List review queue |
| GET | `/api/v1/reviews/{id}` | View review details |
| PUT | `/api/v1/reviews/{id}` | Submit corrections |
| POST | `/api/v1/reviews/{id}/approve` | Approve extraction |
| POST | `/api/v1/reviews/{id}/reject` | Reject & requeue |

---

## Next Steps

1. **Upload a test document** and watch it process
2. **Review extraction results** with confidence scores
3. **Explore the API docs** at http://localhost:8000/docs
4. **Read the design documents**:
   - [Data Model](data-model.md)
   - [Research & Decisions](research.md)
   - [Implementation Plan](plan.md)
5. **Start implementing tasks** (see tasks.md once created)

---

## Getting Help

- **API Issues**: Check logs at `http://localhost:8000/docs` and console output
- **Database Issues**: Use pgAdmin at `http://localhost:5050`
- **Frontend Issues**: Check browser console (F12)
- **Performance Issues**: Monitor with `docker stats`

---

## Stopping Services

```bash
# Stop all services (keep volumes)
docker-compose down

# Stop and remove everything (clean slate)
docker-compose down -v

# Restart specific service
docker-compose restart api
```

---

**You're all set!** Start uploading documents and exploring the system.
