# Research: Document Extraction & Analysis System

**Created**: January 19, 2026  
**Phase**: Phase 0 - Research & Technology Decisions  
**Purpose**: Resolve technology choices and architectural patterns for document processing system

## Research Questions Addressed

### 1. OCR & Document Analysis: Azure Form Recognizer vs Alternatives

**Decision**: Use **Azure Form Recognizer**

**Rationale**: 
- Specifically designed for form/document extraction in enterprise scenarios
- Supports medical forms and structured document layouts
- Provides confidence scores natively (aligns with spec requirement)
- Handles both digital PDFs and scanned images
- Returns structured data with field extraction, not just raw text

**Alternatives Considered**:
- Tesseract OCR: Pure OCR, requires custom NLP for structure extraction (more work)
- AWS Textract: Similar capability, but Form Recognizer has better medical document support
- Google Document AI: Excellent but higher cost and slower iteration

**Implementation Approach**:
- Create wrapper service around Form Recognizer SDK for Python
- Cache trained models for common medical form types
- Implement retry logic with exponential backoff for transient failures
- Monitor API usage and costs

---

### 2. NLP & Entity Recognition: spaCy vs Alternatives

**Decision**: Use **spaCy 3.x** with pre-trained models + custom pipeline

**Rationale**:
- Fast, production-ready NLP library (not experimental)
- Excellent entity extraction performance
- Can be extended with custom entity patterns for medical terminology
- Does not require external service calls (faster than cloud APIs)
- Active community and medical-focused models available

**Alternatives Considered**:
- NLTK: Slower, more suitable for research than production
- Transformers (HuggingFace): Slower inference, overkill for form extraction
- AWS Comprehend Medical: Requires external API calls, adds latency

**Medical Models**:
- Use spaCy's general English model + medical entity patterns
- Custom patterns for: Patient Name, DOB, Medical IDs, Insurance codes
- Can augment with scispaCy (medical-specific) if performance insufficient

**Implementation Approach**:
- Load spaCy model once at service startup
- Define custom entity patterns for medical field types
- Cache entity extraction results to avoid re-processing
- Version control NLP model and entity rules

---

### 3. Database: PostgreSQL Schema Design

**Decision**: Use **PostgreSQL 14+** with SQLAlchemy ORM

**Rationale**:
- Proven for healthcare applications
- ACID compliance for data integrity
- JSON columns for flexible document metadata
- Full-text search for audit log queries
- Strong audit trail support

**Key Tables**:
- `documents`: File metadata, upload timestamps, processing status
- `extraction_results`: Extracted fields with confidence scores
- `extraction_fields`: Individual extracted field values and metadata
- `review_records`: Human review sessions, changes made
- `audit_logs`: All system activities for compliance
- `patients`: Extracted patient entities with relationships

**Design Pattern**: Event Sourcing for audit trail
- All changes are immutable events
- Enables full compliance audit trail
- Supports temporal queries (state at any point in time)

---

### 4. Async Task Processing: Celery + Redis

**Decision**: Use **Celery with Redis** for batch processing

**Rationale**:
- Celery is industry-standard for async Python task queues
- Redis provides fast, reliable task queue storage
- Supports priority queues (urgent reviews prioritized)
- Built-in retry logic and dead-letter queues
- Scales to thousands of tasks per day

**Alternative**: Direct async with asyncio
- Insufficient for batch resilience
- No task persistence if process crashes
- Cannot easily scale across multiple workers

**Implementation Approach**:
- Celery task: Process single document (OCR + extraction + NLP)
- Task retries with exponential backoff on Azure API failures
- Dead-letter queue for permanently failed documents
- Monitoring via Flower (Celery monitoring tool)
- Redis as broker with AOF persistence for reliability

---

### 5. REST API Framework: FastAPI

**Decision**: Use **FastAPI** for REST API

**Rationale**:
- Native async support (better performance than Flask/Django for I/O-bound tasks)
- Auto-generated OpenAPI documentation (satisfies spec requirement)
- Built-in input validation with Pydantic
- Modern Python (3.7+ with type hints)
- Rapid API development

**Alternative**: Django REST Framework
- More mature, but heavier overhead
- Overkill for document processing API
- Slower async support

**API Design**:
- `/api/documents` - upload, list documents
- `/api/documents/{id}/status` - check processing status
- `/api/documents/{id}/results` - retrieve extracted data
- `/api/reviews` - list documents awaiting review
- `/api/reviews/{id}` - get/update review record
- `/api/health` - system health check

---

### 6. Frontend Framework: React + TypeScript

**Decision**: Use **React 18+ with TypeScript** for dashboard

**Rationale**:
- Component-based reusability (Document list, Review form, Dashboard layout)
- TypeScript prevents runtime errors in data display
- Rich ecosystem of UI libraries (Material-UI, React Query)
- Better performance than server-side rendering for dashboard

**UI Components**:
- DocumentList: Searchable, filterable table of documents with confidence scores
- ReviewDetail: Side-by-side document + extraction form with edit capability
- DashboardMetrics: Real-time processing stats and queue status

**State Management**: React Query for server state, Redux only if needed later

---

### 7. Batch Processing Architecture: Job Queue Pattern

**Decision**: **Celery task queue with priority levels**

**Rationale**:
- Spec requires "batch processing of 100+ documents without blocking UI"
- Celery enables async processing with monitoring
- Multiple workers scale horizontally
- Priority queue for urgent human reviews

**Flow**:
1. User uploads batch via API
2. Documents queued in Celery with priority (default: medium)
3. Workers process documents in parallel
4. Results stored to PostgreSQL
5. Client polls `/api/documents/{batch_id}/status` for progress
6. Auto-flag low-confidence documents for immediate review

**Scaling**:
- Start with 2-3 Celery workers locally
- Cloud deployment: auto-scaling Kubernetes pods
- Redis cluster for distributed task queue

---

### 8. Confidence Scoring Algorithm

**Decision**: **Composite scoring from multiple signals**

**Rationale**:
- Spec requires confidence score 0.0-1.0 per field
- Single source insufficient (e.g., Azure Form Recognizer score alone not enough)

**Scoring Components**:
1. **Azure Form Recognizer confidence** (50% weight):
   - Direct output from Azure API
   
2. **OCR quality** (20% weight):
   - Document clarity, resolution, text legibility
   - Lower for scanned low-quality images
   
3. **NLP entity match quality** (20% weight):
   - spaCy entity confidence
   - Pattern match specificity
   
4. **Data validation** (10% weight):
   - Format validation (date is valid, email matches pattern, etc)
   - Dictionary validation (state codes, known medical IDs)

**Formula**: 
```
confidence = 0.5 * azure_score + 0.2 * ocr_quality + 0.2 * nlp_confidence + 0.1 * validation_score
```

**Flag Rule**: If confidence < 0.8, automatically flag for human review

---

### 9. Logging & Observability

**Decision**: **Structured logging with centralized aggregation**

**Rationale**:
- Spec requires "comprehensive error handling with logging"
- Healthcare requires compliance audit trails
- Production debugging requires structured data

**Implementation**:
- Python `structlog` library for structured JSON logs
- Log fields: timestamp, service, level, trace_id, user_id, action, document_id
- Store to: stdout (container logs) + centralized log system (ELK or CloudWatch)
- Query-able via trace_id for full audit trail of document processing

**Log Levels**:
- ERROR: Failures requiring attention (API errors, extraction failures)
- WARNING: Degraded states (low confidence, slow processing)
- INFO: Business events (document uploaded, review approved)
- DEBUG: Detailed execution (field extraction details, API calls)

---

### 10. Local Development Environment

**Decision**: **Docker Compose for reproducibility**

**Rationale**:
- Spec requires "new developers setup in under 30 minutes"
- Docker ensures consistency: macOS, Linux, Windows all identical
- Eliminates "works on my machine" problems

**Containers**:
- PostgreSQL 14 (database)
- Redis (task queue)
- API backend (Python/FastAPI)
- Frontend (React dev server with hot-reload)
- pgAdmin (database management UI)

**Setup Time**: 
- Clone repo → `docker-compose up` → 5 minutes
- Ready to make code changes and see live reload

---

### 11. Testing Strategy

**Decision**: **Three-tier testing pyramid**

**Rationale**: 
- Spec requires testable, production-ready code
- Different test types catch different issues

**Test Tiers**:

1. **Unit Tests** (70% coverage target):
   - Service logic: extraction, scoring, validation
   - Models: Pydantic validation
   - Utilities: field parsing, format conversion
   - Tool: `pytest`, run locally in seconds

2. **Integration Tests** (20% coverage):
   - API endpoint contracts
   - Database operations (with test database)
   - Celery task execution
   - Tool: `pytest` with fixtures, run pre-commit

3. **End-to-End Tests** (10% coverage):
   - Full user workflows: upload → extract → review → approve
   - Dashboard UI interactions
   - Tool: `Playwright`, run in CI/CD only

**CI/CD Gate**: All tests must pass before merge; coverage must not decrease

---

### 12. Deployment & Containerization

**Decision**: **Docker containers + Docker Compose** for local, **Kubernetes** for production

**Rationale**:
- Spec requires "support containerized deployment (Docker)"
- Single container image for API backend
- Separate container for Celery workers (can scale independently)
- Kubernetes enables horizontal scaling

**Container Strategy**:
- Multi-stage Docker builds to minimize image size
- Base image: `python:3.11-slim` (minimal)
- Separate production (`Dockerfile`) and dev (`Dockerfile.dev`) images
- Image tagging: `signupreader-api:v1.0.0`, `signupreader-frontend:v1.0.0`

**Production Deployment**:
- Kubernetes StatefulSet for API (sticky sessions for review continuity)
- Kubernetes Deployment for Celery workers (stateless, auto-scaling)
- PostgreSQL as managed service (RDS/Cloud SQL)
- Redis as managed service (ElastiCache/MemoryStore)

---

## Summary of Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.11+ | Fast development, mature libraries |
| Web Framework | FastAPI | Async, auto-docs, modern |
| NLP | spaCy 3.x | Production-ready entity extraction |
| OCR | Azure Form Recognizer | Structured form extraction + confidence scores |
| Database | PostgreSQL 14+ | ACID, healthcare-ready, audit support |
| Async Tasks | Celery + Redis | Batch processing, scalability |
| Frontend | React 18+ + TypeScript | Component reusability, type safety |
| Testing | pytest + Playwright | Comprehensive, fast feedback |
| Container | Docker + Docker Compose | Reproducibility, local dev |
| Deployment | Kubernetes | Horizontal scaling, cloud-native |
| Observability | structlog + centralized logging | Compliance audit trails |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    React Dashboard                      │
│         (Document list, review form, metrics)           │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────────────┐
│            FastAPI Backend (Port 8000)                  │
│  - Document upload / listing                            │
│  - Review management                                    │
│  - Health checks & metrics                              │
└──┬─────────────────────────────────────────┬────────────┘
   │                                         │
   │ Submit task                             │ Query results
   │                                         │
┌──▼─────────────────────┐    ┌──────────────▼────────────┐
│ Celery Workers         │    │ PostgreSQL Database       │
│ (Batch processing)     │    │  - Documents              │
│                        │    │  - ExtractionResults      │
│ 1. Azure Form          │    │  - ReviewRecords          │
│    Recognizer          │    │  - AuditLogs              │
│ 2. spaCy NLP           │    │  - Patients               │
│ 3. Confidence scoring  │    └──────────────────────────┘
│ 4. Store results       │
└──┬─────────────────────┘
   │
   └──────────┬──────────────┐
              │              │
    ┌─────────▼──┐  ┌────────▼─────┐
    │    Redis   │  │ Azure Form    │
    │ (Task Q)   │  │ Recognizer    │
    └────────────┘  │ (Cloud API)   │
                    └───────────────┘
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Azure API quota exhausted | Implement rate limiting, batch API calls, quotas per day |
| Low extraction accuracy | Extensive testing, confidence scoring, manual review for <0.8 |
| Database performance degrades | Indexes on document_id/status, partition audit logs by date |
| Celery worker crashes | Task retries (3x with backoff), persistent Redis queue |
| Compliance audit trail gaps | All operations logged, immutable event stream, quarterly audits |

---

## Next Steps

1. **Phase 1** ➜ Create data model and API contracts
2. **Phase 1** ➜ Set up local development environment (Docker Compose)
3. **Phase 2** ➜ Break down into implementation tasks
4. **Implementation** ➜ Start with document upload + basic extraction
