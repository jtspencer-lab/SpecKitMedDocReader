# Tasks: Document Extraction & Analysis System

**Input**: Design documents from `/specs/001-document-extraction/`  
**Prerequisites**: spec.md, plan.md, research.md, data-model.md, contracts/api.openapi.yaml, quickstart.md  
**Branch**: `001-document-extraction`  
**Total Tasks**: 92 across 8 phases

## Format Guide

- **[P]**: Task can run in parallel (independent files, no dependencies on incomplete tasks)
- **[Story]**: User story label - US1, US2, US3, US4, US5, US6
- Exact file paths provided for all tasks

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Initialize project structure and core infrastructure foundation

**Duration**: 2-3 days  
**Team**: 1 developer  
**Deliverable**: Runnable project with database and API server starting successfully

- [X] T001 Create project directory structure per plan.md in backend/ and frontend/ directories
- [X] T002 Initialize Python backend with pyproject.toml dependencies (FastAPI, SQLAlchemy, spaCy, etc.) in backend/pyproject.toml
- [X] T003 [P] Initialize frontend Node project with package.json and React dependencies in frontend/package.json
- [X] T004 [P] Create docker-compose.yml with PostgreSQL, Redis, API, frontend, pgAdmin services
- [X] T005 [P] Create .env.example with all environment variables and documentation in .env.example
- [X] T006 Create backend/main.py with FastAPI application initialization and startup/shutdown events
- [X] T007 [P] Create frontend/src/App.tsx root component with routing structure
- [X] T008 Create backend/Dockerfile and backend/Dockerfile.dev for containerization
- [X] T009 [P] Create frontend Dockerfile for React development and production builds
- [X] T010 Create .dockerignore and .gitignore files for repository root
- [X] T011 [P] Configure pytest in backend/pyproject.toml with test discovery and coverage settings
- [X] T012 [P] Configure Jest in frontend/package.json for React component testing
- [X] T013 Create backend/README.md with project overview, setup, and development guidelines
- [X] T014 [P] Create frontend/README.md with project overview, setup, and development guidelines
- [X] T015 Verify docker-compose up successfully starts all services (run locally: 5-10 min startup)

**Checkpoint**: Project structure ready, all containers start without errors

---

## Phase 2: Foundational Infrastructure (Blocking Prerequisites)

**Purpose**: Core database, API framework, and infrastructure that MUST be complete before any user story implementation

**Duration**: 5-7 days  
**Team**: 2-3 developers (database specialist, backend lead, frontend lead)  
**Deliverable**: API server running with database connected, health checks passing, error handling framework in place

### Database & Migration Infrastructure

- [X] T016 Create backend/src/db/base.py with SQLAlchemy Base class and database session management
- [X] T017 Create backend/src/db/session.py with database connection pool and session factory
- [X] T018 Create backend/alembic.ini configuration for database migrations
- [X] T019 Create backend/migrations/env.py for Alembic migration environment
- [X] T020 Create initial migration template in backend/migrations/versions/001_initial_schema.py (skeleton only, populated later)
- [X] T021 Create database initialization script backend/src/db/init_db.py for test database setup

### Core Models & Schemas

- [X] T022 [P] Create backend/src/models/common.py with base UUID, timestamp mixins
- [X] T023 [P] Create backend/src/models/document.py with Document SQLAlchemy model (schema only, no relationships yet)
- [X] T024 [P] Create backend/src/models/extraction.py with ExtractionResult and ExtractionField models
- [X] T025 [P] Create backend/src/models/review.py with ReviewRecord model
- [X] T026 [P] Create backend/src/models/audit.py with AuditLog model
- [X] T027 [P] Create backend/src/models/patient.py with Patient model
- [X] T028 [P] Create backend/src/models/__init__.py exporting all models for SQLAlchemy
- [X] T029 Create backend/src/schemas/document.py with Pydantic DocumentResponse, DocumentUploadResponse schemas
- [X] T030 [P] Create backend/src/schemas/extraction.py with ExtractionResultResponse, ExtractionFieldData schemas
- [X] T031 [P] Create backend/src/schemas/review.py with ReviewDetailsResponse, ReviewUpdateRequest schemas
- [X] T032 Create backend/src/schemas/__init__.py for schema exports

### API Infrastructure

- [X] T033 Create backend/src/api/__init__.py with APIRouter setup
- [X] T034 Create backend/src/api/dependencies.py with dependency injection (get_db, get_current_user, etc.)
- [X] T035 Create backend/src/api/routes/__init__.py for route organization
- [X] T036 Create backend/src/api/middleware.py with error handling, request logging middleware
- [X] T037 Create backend/src/utils/errors.py with custom exception classes and error handlers
- [X] T038 Create backend/src/utils/logging.py with structlog configuration for JSON logging
- [X] T039 [P] Create backend/src/config.py with environment-based configuration (dev, test, prod)
- [X] T040 Create backend/main.py application factory with middleware, error handlers, startup

### Celery & Task Queue Setup

- [X] T041 Create backend/src/tasks/__init__.py with Celery app initialization
- [X] T042 Create backend/src/tasks/config.py with Celery broker and result backend configuration
- [X] T043 Create backend/celery_worker.py entry point for running Celery workers
- [X] T044 Create docker-compose service definitions for Redis and Celery worker containers

### Frontend Infrastructure

- [X] T045 Create frontend/src/types/index.ts with TypeScript interfaces for API responses
- [X] T046 Create frontend/src/services/api.ts with Axios/fetch client for API calls
- [X] T047 Create frontend/src/services/auth.ts with authentication token management
- [X] T048 Create frontend/src/components/Layout.tsx with header, nav, footer structure
- [X] T049 Create frontend/src/pages/Home.tsx root landing page component
- [X] T050 Set up React Router in frontend/src/App.tsx with route definitions

### Testing Infrastructure

- [X] T051 Create backend/tests/__init__.py with pytest fixtures and conftest.py
- [X] T052 Create backend/tests/conftest.py with database fixtures, client fixtures
- [X] T053 Create backend/tests/contract/README.md documenting API contract testing approach
- [X] T054 Create frontend/jest.config.js with React Testing Library configuration
- [X] T055 Create frontend/tests/setup.ts with test utilities and mocks

### Health Check & Verification

- [X] T056 Create backend/src/api/routes/health.py with /health endpoint
- [X] T057 Implement health check in backend/main.py checking database, Redis, external APIs
- [X] T058 Update docker-compose.yml to add healthcheck for API container
- [X] T059 Verify database migrations run successfully: `docker-compose exec api alembic upgrade head`
- [X] T060 Verify API starts and returns 200 from /health endpoint
- [ ] T061 Verify frontend builds and serves at http://localhost:3000

**Checkpoint**: Foundation complete. Database connected, API responding, test infrastructure ready. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Document Upload & Extraction (Priority: P1)

**Goal**: Users can upload medical documents and automatically extract structured data with confidence scoring

**Independent Test**: Upload a PDF document via web UI, polling shows "completed", results show extracted fields with confidence scores

**Duration**: 5-7 days  
**Team**: 3-4 developers (backend: document processing, OCR integration; frontend: upload form, progress tracking)

### Tests for User Story 1 (TDD - Write FIRST, ensure FAIL before implementation)

- [ ] T062 [P] [US1] Contract test: POST /api/v1/documents upload endpoint returns 201 with document_id in backend/tests/contract/test_document_upload.py
- [ ] T063 [P] [US1] Contract test: GET /api/v1/documents/{id}/status returns processing status in backend/tests/contract/test_document_status.py
- [ ] T064 [P] [US1] Contract test: GET /api/v1/documents/{id}/results returns extraction results after completion in backend/tests/contract/test_extraction_results.py
- [ ] T065 [P] [US1] Integration test: Full document upload → processing → results retrieval in backend/tests/integration/test_document_workflow.py
- [ ] T066 [P] [US1] Integration test: Celery task processes document and stores results in database in backend/tests/integration/test_extraction_task.py
- [ ] T067 [P] [US1] Unit test: Document service validates file format and size in backend/tests/unit/test_document_service.py
- [ ] T068 [P] [US1] Unit test: ExtractionField model validates confidence scores (0.0-1.0) in backend/tests/unit/test_extraction_model.py

### Implementation for User Story 1

#### Backend: Document & Extraction Services

- [ ] T069 [P] [US1] Create backend/src/services/document_service.py with DocumentService class for document management
- [ ] T070 [P] [US1] Implement DocumentService.create_document() to save uploaded document metadata to database
- [ ] T071 [P] [US1] Implement DocumentService.get_document() and get_document_list() queries
- [ ] T072 [P] [US1] Create backend/src/services/extraction_service.py with ExtractionService for managing extraction results
- [ ] T073 [US1] Implement ExtractionService.calculate_confidence_score() using composite algorithm (research.md)
- [ ] T074 [P] [US1] Create backend/src/services/azure_service.py wrapper around Azure Form Recognizer SDK
- [ ] T075 [US1] Implement AzureService.extract_from_document() calling Form Recognizer API with error handling
- [ ] T076 [P] [US1] Create backend/src/services/nlp_service.py wrapper around spaCy for entity extraction
- [ ] T077 [US1] Implement NLPService.extract_entities() loading spaCy model and extracting medical entities
- [ ] T078 [P] [US1] Create backend/src/tasks/extraction_tasks.py with Celery tasks
- [ ] T079 [US1] Implement task: process_document() - orchestrates OCR, NLP, confidence scoring, stores results
- [ ] T080 [US1] Implement retry logic in process_document() with exponential backoff for transient failures
- [ ] T081 [P] [US1] Implement DocumentService.get_extraction_status() returning processing progress

#### Backend: API Endpoints

- [ ] T082 [P] [US1] Create backend/src/api/routes/documents.py with document endpoints
- [ ] T083 [US1] Implement POST /api/v1/documents - file upload, validation, queue for processing
- [ ] T084 [US1] Implement GET /api/v1/documents - list documents with pagination and filtering
- [ ] T085 [US1] Implement GET /api/v1/documents/{id} - get document details
- [ ] T086 [US1] Implement GET /api/v1/documents/{id}/status - return processing status and progress
- [ ] T087 [US1] Implement GET /api/v1/documents/{id}/results - return extraction results (202 if still processing)
- [ ] T088 [US1] Add validation for file format, size, content-type in document routes
- [ ] T089 [P] [US1] Add audit logging for all document operations in routes

#### Frontend: Document Upload & Results View

- [ ] T090 [P] [US1] Create frontend/src/components/DocumentUpload.tsx with file input and upload form
- [ ] T091 [US1] Implement file validation (format, size) on frontend before sending
- [ ] T092 [US1] Implement progress tracking by polling /api/v1/documents/{id}/status
- [ ] T093 [P] [US1] Create frontend/src/components/ExtractionResults.tsx displaying extracted fields
- [ ] T094 [P] [US1] Highlight fields by confidence score (green: >0.9, yellow: 0.8-0.9, red: <0.8)
- [ ] T095 [US1] Create frontend/src/pages/DocumentUploadPage.tsx orchestrating upload and results display
- [ ] T096 [US1] Implement auto-refresh of status every 2 seconds until completion
- [ ] T097 [P] [US1] Create frontend/src/components/ConfidenceScoreBadge.tsx for visual confidence indication
- [ ] T098 [P] [US1] Add error state and retry logic on frontend

#### Database Migrations

- [ ] T099 [US1] Create database migration to create documents, extraction_results, extraction_fields tables
- [ ] T100 [US1] Add indexes for document status and date queries

**Checkpoint**: User Story 1 complete. Users can upload documents, see extraction results with confidence scores. Ready for US2 (review flagging depends on US1 extraction).

---

## Phase 4: User Story 2 - Confidence Scoring & Review Flagging (Priority: P1)

**Goal**: Extracted fields with low confidence are automatically flagged for human review

**Independent Test**: Upload document, verify fields with confidence < 0.8 appear in review queue flagged

**Duration**: 3-4 days  
**Team**: 2-3 developers (backend: flagging logic; frontend: review queue display)

**Dependencies**: Depends on User Story 1 (extraction must complete before flagging)

### Tests for User Story 2

- [ ] T101 [P] [US2] Unit test: ExtractionService.flag_low_confidence_fields() marks fields <0.8 for review in backend/tests/unit/test_confidence_scoring.py
- [ ] T102 [P] [US2] Integration test: Fields automatically flagged when extraction completes in backend/tests/integration/test_review_flagging.py
- [ ] T103 [P] [US2] Contract test: GET /api/v1/reviews returns flagged fields sorted by confidence in backend/tests/contract/test_review_queue.py

### Implementation for User Story 2

#### Backend: Flagging Logic

- [ ] T104 [US2] Implement ExtractionService.flag_low_confidence_fields() marking fields with confidence < 0.8
- [ ] T105 [US2] Create ReviewRecord when extraction completes and fields are flagged
- [ ] T106 [P] [US2] Implement automatic review record creation in process_document task (after extraction, before storing)
- [ ] T107 [P] [US2] Create backend/src/services/review_service.py with ReviewService for review management
- [ ] T108 [US2] Implement ReviewService.get_pending_reviews() querying flagged documents
- [ ] T109 [US2] Implement ReviewService.get_review_detail() returning extraction + flagged fields

#### Backend: Review API Endpoints

- [ ] T110 [P] [US2] Create backend/src/api/routes/reviews.py with review endpoints
- [ ] T111 [US2] Implement GET /api/v1/reviews - list documents awaiting review, sorted by confidence (lowest first)
- [ ] T112 [US2] Implement GET /api/v1/reviews/{id} - get review details with extraction results
- [ ] T113 [P] [US2] Add pagination and filtering by reviewer_id

#### Frontend: Review Queue Display

- [ ] T114 [P] [US2] Create frontend/src/components/ReviewQueue.tsx displaying pending documents
- [ ] T115 [P] [US2] Display overall confidence score for each document
- [ ] T116 [P] [US2] Display flagged field count and indication which fields need review
- [ ] T117 [US2] Sort by confidence score ascending (lowest priority first)
- [ ] T118 [P] [US2] Create frontend/src/pages/ReviewQueuePage.tsx with queue list and navigation
- [ ] T119 [P] [US2] Add click-to-review navigation linking to review detail page

**Checkpoint**: Review flagging working. Documents with low-confidence extractions appear in review queue. Ready for US3 (review editing).

---

## Phase 5: User Story 3 - Human Review Dashboard (Priority: P1)

**Goal**: Reviewers can view flagged extractions side-by-side with original document and approve/reject/correct

**Independent Test**: Navigate to review detail, see extraction fields in form, edit field, click approve, document removed from queue

**Duration**: 6-8 days  
**Team**: 4-5 developers (backend: correction persistence, audit logging; frontend: review form, document viewer)

**Dependencies**: Depends on User Story 1 & 2 (extraction and flagging must be working)

### Tests for User Story 3

- [ ] T120 [P] [US3] Contract test: PUT /api/v1/reviews/{id} updates extraction with corrections in backend/tests/contract/test_review_update.py
- [ ] T121 [P] [US3] Contract test: POST /api/v1/reviews/{id}/approve marks document approved in backend/tests/contract/test_review_approve.py
- [ ] T122 [P] [US3] Contract test: POST /api/v1/reviews/{id}/reject requeues document in backend/tests/contract/test_review_reject.py
- [ ] T123 [P] [US3] Integration test: Review corrections persisted and audit-logged in backend/tests/integration/test_review_workflow.py
- [ ] T124 [P] [US3] Unit test: ReviewService handles field updates and status transitions in backend/tests/unit/test_review_service.py

### Implementation for User Story 3

#### Backend: Review Update & Status Management

- [ ] T125 [US3] Extend ReviewService with update_review() accepting field corrections
- [ ] T126 [US3] Implement ReviewService.approve_review() marking review approved, removing from queue
- [ ] T127 [US3] Implement ReviewService.reject_review() requeuing document for reprocessing
- [ ] T128 [P] [US3] Implement ReviewService.get_review_detail() returning full extraction + review history
- [ ] T129 [US3] Create backend/src/services/audit_service.py for logging all review actions
- [ ] T130 [US3] Implement AuditService.log_review_action() recording all changes (user, timestamp, field changes)
- [ ] T131 [P] [US3] Create ReviewChange tracking in review update - record old_value, new_value, timestamp

#### Backend: Review API Endpoints

- [ ] T132 [US3] Implement PUT /api/v1/reviews/{id} - accept field corrections, update database
- [ ] T133 [US3] Implement POST /api/v1/reviews/{id}/approve - approve review, create audit log
- [ ] T134 [US3] Implement POST /api/v1/reviews/{id}/reject - reject review with reason, requeue document
- [ ] T135 [P] [US3] Add validation ensuring all flagged fields are reviewed before approval
- [ ] T136 [P] [US3] Add error handling for concurrent edits (optimistic locking or version check)

#### Frontend: Review Detail Page

- [ ] T137 [P] [US3] Create frontend/src/pages/ReviewDetailPage.tsx with layout for document + form
- [ ] T138 [P] [US3] Create frontend/src/components/DocumentViewer.tsx displaying original document/image
- [ ] T139 [US3] Support PDF viewing (use react-pdf or similar library)
- [ ] T140 [P] [US3] Support image viewing (JPEG, PNG, TIFF)
- [ ] T141 [P] [US3] Implement zoom and navigation for document viewing

#### Frontend: Review Form & Corrections

- [ ] T142 [P] [US3] Create frontend/src/components/ExtractionReviewForm.tsx with editable fields
- [ ] T143 [P] [US3] Display each extracted field in form with original value and confidence score
- [ ] T144 [P] [US3] Allow editing of low-confidence fields (<0.8)
- [ ] T145 [P] [US3] Highlight fields by confidence (color coding)
- [ ] T146 [US3] Implement Save Corrections button - PUT /api/v1/reviews/{id} with changes
- [ ] T147 [P] [US3] Implement Approve button - POST /api/v1/reviews/{id}/approve
- [ ] T148 [P] [US3] Implement Reject button with reason modal - POST /api/v1/reviews/{id}/reject
- [ ] T149 [US3] Show success/error messages on submission
- [ ] T150 [P] [US3] Navigate back to review queue after approval/rejection

#### Frontend: Additional UI

- [ ] T151 [P] [US3] Create frontend/src/components/FieldDiffViewer.tsx showing original vs corrected value
- [ ] T152 [P] [US3] Create frontend/src/components/AuditTrail.tsx showing review history and changes
- [ ] T153 [P] [US3] Add toggle to show/hide reviewed vs flagged fields

#### Database & Audit

- [ ] T154 [US3] Create ReviewRecord and AuditLog table migration if not already done
- [ ] T155 [US3] Verify audit log entries created for all review actions

**Checkpoint**: Full review workflow operational. Reviewers can edit extractions, approve/reject documents. Documents flow through complete workflow.

---

## Phase 6: User Story 4 - Batch Processing & Scalability (Priority: P2)

**Goal**: Users can upload 100+ documents and monitor overall batch progress without UI blocking

**Independent Test**: Upload 100 documents via batch upload, see progress tracking updating, all documents eventually processed

**Duration**: 5-6 days  
**Team**: 3-4 developers (backend: batch orchestration, progress tracking; frontend: batch upload, progress UI)

**Dependencies**: Works alongside User Stories 1-3, but independent of their completion

### Tests for User Story 4

- [ ] T156 [P] [US4] Contract test: POST /api/v1/batch/upload returns batch_id in backend/tests/contract/test_batch_upload.py
- [ ] T157 [P] [US4] Contract test: GET /api/v1/batch/{id}/status returns progress counts in backend/tests/contract/test_batch_status.py
- [ ] T158 [P] [US4] Integration test: Batch with 100 documents processes all without errors in backend/tests/integration/test_batch_processing.py
- [ ] T159 [P] [US4] Integration test: Failed document in batch doesn't block others in backend/tests/integration/test_batch_error_handling.py
- [ ] T160 [P] [US4] Performance test: 100 documents complete within time target in backend/tests/integration/test_batch_performance.py

### Implementation for User Story 4

#### Backend: Batch Processing

- [ ] T161 [P] [US4] Create backend/src/models/batch.py with Batch model tracking batch metadata and progress
- [ ] T162 [P] [US4] Extend DocumentService with batch operations
- [ ] T163 [US4] Implement DocumentService.create_batch() initializing batch record
- [ ] T164 [US4] Implement DocumentService.add_documents_to_batch() queuing multiple documents
- [ ] T165 [P] [US4] Create backend/src/services/batch_service.py with BatchService
- [ ] T166 [US4] Implement BatchService.get_batch_progress() calculating completion percentages
- [ ] T167 [P] [US4] Implement batch task coordination in extraction_tasks.py
- [ ] T168 [US4] Ensure Celery workers process documents concurrently (multiple workers, connection pool)
- [ ] T169 [P] [US4] Implement dead-letter queue for permanently failed documents

#### Backend: Batch API Endpoints

- [ ] T170 [P] [US4] Create backend/src/api/routes/batch.py with batch endpoints
- [ ] T171 [US4] Implement POST /api/v1/batch/upload - accept multiple files, create batch, queue all
- [ ] T172 [US4] Implement GET /api/v1/batch/{id}/status - return batch progress (total, completed, failed, pending)
- [ ] T173 [US4] Implement GET /api/v1/batch/{id}/documents - list all documents in batch with individual status

#### Frontend: Batch Upload

- [ ] T174 [P] [US4] Create frontend/src/components/BatchUploadForm.tsx with multi-file drag-drop
- [ ] T175 [P] [US4] Implement file selection (100+ files support)
- [ ] T176 [US4] Implement batch upload POST request
- [ ] T177 [P] [US4] Create frontend/src/pages/BatchUploadPage.tsx orchestrating upload and tracking

#### Frontend: Batch Progress Tracking

- [ ] T178 [P] [US4] Create frontend/src/components/BatchProgress.tsx with overall progress bar
- [ ] T179 [P] [US4] Display counts: total, completed, failed, pending
- [ ] T180 [P] [US4] Display estimated time remaining
- [ ] T181 [US4] Implement auto-refresh of batch status every 3 seconds during processing
- [ ] T182 [P] [US4] Show individual document status in expandable list
- [ ] T183 [P] [US4] Show error details for failed documents

#### Database

- [ ] T184 [US4] Create Batch model migration if not done yet
- [ ] T185 [US4] Add batch_id foreign key to Document model if needed

**Checkpoint**: Batch upload and progress tracking operational. Users can upload large batches and monitor completion.

---

## Phase 7: User Story 5 - REST API for Integration (Priority: P2)

**Goal**: Third-party systems can programmatically upload documents and retrieve results via documented REST API

**Independent Test**: Make curl requests to upload document and retrieve results, verify OpenAPI docs at /docs show all endpoints

**Duration**: 4-5 days  
**Team**: 2-3 developers (backend: API completion and docs; frontend: minimal, API testing)

**Dependencies**: Builds on Stories 1-4, completes API coverage

### Tests for User Story 5

- [ ] T186 [P] [US5] Contract test: All OpenAPI endpoints return expected schemas in backend/tests/contract/test_openapi_validation.py
- [ ] T187 [P] [US5] Integration test: Third-party library can use auto-generated client in backend/tests/integration/test_api_client_generation.py
- [ ] T188 [P] [US5] Integration test: Error responses follow consistent error schema in backend/tests/integration/test_error_responses.py

### Implementation for User Story 5

#### Backend: API Enhancement

- [ ] T189 [US5] Verify all 16 endpoints from contracts/api.openapi.yaml are implemented
- [ ] T190 [P] [US5] Implement GET /api/v1/documents/list alternative endpoint if needed
- [ ] T191 [US5] Ensure all responses match OpenAPI schema definitions
- [ ] T192 [P] [US5] Implement consistent error response format per OpenAPI spec
- [ ] T193 [P] [US5] Add Bearer token validation to all protected endpoints
- [ ] T194 [P] [US5] Implement rate limiting (e.g., 100 requests/minute per API key)
- [ ] T195 [US5] Add API key/token model to database for third-party auth
- [ ] T196 [P] [US5] Create API key management endpoints for admin (create, revoke, list keys)

#### Backend: OpenAPI & Documentation

- [ ] T197 [US5] Update FastAPI app to auto-serve OpenAPI spec at /api/docs
- [ ] T198 [US5] Verify Swagger UI works at http://localhost:8000/docs
- [ ] T199 [US5] Verify ReDoc available at http://localhost:8000/redoc
- [ ] T200 [US5] Add examples to all API schemas in OpenAPI spec
- [ ] T201 [P] [US5] Generate Python client library from OpenAPI spec (using openapi-generator)
- [ ] T202 [P] [US5] Generate TypeScript client library from OpenAPI spec
- [ ] T203 [US5] Create API usage examples in backend/docs/api-examples.md

#### Testing & Validation

- [ ] T204 [P] [US5] Validate OpenAPI spec: spec/001-document-extraction/contracts/api.openapi.yaml
- [ ] T205 [US5] Test all endpoints with Postman/Insomnia collection: backend/docs/postman-collection.json
- [ ] T206 [P] [US5] Create integration test script making requests from third-party perspective

**Checkpoint**: REST API fully implemented, documented, and ready for external integration.

---

## Phase 8: User Story 6 - Audit Logging & Compliance (Priority: P2)

**Goal**: All document processing and review activities are logged with full audit trail for HIPAA compliance

**Independent Test**: Perform actions (upload, extract, review, approve), verify AuditLog entries exist with timestamp, user, action, changes

**Duration**: 4-5 days  
**Team**: 2-3 developers (backend: audit logging integration; frontend: audit log viewing)

**Dependencies**: Parallel work on Stories 1-5, audit logging integrated into existing endpoints

### Tests for User Story 6

- [ ] T207 [P] [US6] Unit test: AuditService logs all required action types in backend/tests/unit/test_audit_logging.py
- [ ] T208 [P] [US6] Integration test: AuditLog entries created for document upload, extraction, review in backend/tests/integration/test_audit_trail.py
- [ ] T209 [P] [US6] Contract test: GET /api/v1/audit-logs returns queryable audit entries in backend/tests/contract/test_audit_logs.py
- [ ] T210 [P] [US6] Compliance test: All PII operations logged with user_id, timestamp in backend/tests/integration/test_compliance_logging.py

### Implementation for User Story 6

#### Backend: Audit Logging Infrastructure

- [ ] T211 [US6] Extend AuditService with logging for all action types from research.md
- [ ] T212 [P] [US6] Create middleware in backend/src/api/middleware.py to capture request/response for audit
- [ ] T213 [US6] Implement audit log creation in all API handlers (document upload, extraction, review, etc)
- [ ] T214 [P] [US6] Add change_data tracking for field modifications (old_value, new_value)
- [ ] T215 [P] [US6] Add IP address capture for audit trail
- [ ] T216 [P] [US6] Create audit log queries: by date range, by user, by action, by entity
- [ ] T217 [US6] Implement export audit logs to CSV/JSON for compliance reports
- [ ] T218 [P] [US6] Ensure AuditLog is append-only (no updates, no deletes)

#### Backend: Audit API Endpoints

- [ ] T219 [US6] Implement GET /api/v1/audit-logs with filtering by date range, user_id, action
- [ ] T220 [US6] Implement audit log pagination
- [ ] T221 [P] [US6] Add admin authentication check (audit logs require elevated permissions)
- [ ] T222 [US6] Implement GET /api/v1/audit-logs/export to download as CSV

#### Frontend: Audit Log Viewing (Dashboard)

- [ ] T223 [P] [US6] Create frontend/src/pages/AdminDashboard.tsx with compliance tools
- [ ] T224 [P] [US6] Create frontend/src/components/AuditLogViewer.tsx displaying audit entries
- [ ] T225 [P] [US6] Implement date range picker for audit log filtering
- [ ] T226 [P] [US6] Implement user filter dropdown
- [ ] T227 [P] [US6] Implement action type filter
- [ ] T228 [US6] Display audit log table with: timestamp, user, action, entity, details
- [ ] T229 [P] [US6] Add export to CSV button
- [ ] T230 [P] [US6] Add search bar for entity_id or change_data text search

#### Compliance & Privacy

- [ ] T231 [US6] Implement column-level encryption for SSN and PII fields in patient table
- [ ] T232 [P] [US6] Add field-level access logging (log reads of sensitive fields)
- [ ] T233 [P] [US6] Create HIPAA compliance checklist in backend/docs/hipaa-compliance.md
- [ ] T234 [US6] Document data retention policies in backend/docs/data-retention.md

**Checkpoint**: Full audit trail operational. All user actions logged. Compliance reporting available.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, performance optimization, security hardening

**Duration**: 3-4 days  
**Team**: 2-3 developers (full stack)

### Documentation & Setup

- [ ] T235 [P] Run quickstart.md setup and verify complete in <30 minutes on clean machine
- [ ] T236 [P] Complete backend/README.md with architecture diagrams and coding guidelines
- [ ] T237 [P] Complete frontend/README.md with component structure and styling guidelines
- [ ] T238 Create backend/docs/database-schema.md with entity relationships and index strategy
- [ ] T239 [P] Create backend/docs/api-security.md documenting auth, rate limiting, CORS
- [ ] T240 [P] Create deployment guide backend/docs/deployment.md for Docker, Kubernetes

### Testing & Coverage

- [ ] T241 Run full backend test suite: `pytest --cov=src tests/ --cov-report=html`
- [ ] T242 Ensure backend test coverage >80%
- [ ] T243 [P] Run full frontend test suite: `npm test -- --coverage`
- [ ] T244 [P] Ensure frontend test coverage >75%
- [ ] T245 Run end-to-end tests with Playwright: `npm run test:e2e`
- [ ] T246 [P] Document known limitations and future improvements in backend/FUTURE.md

### Performance & Optimization

- [ ] T247 Profile database queries, add missing indexes if identified
- [ ] T248 Test extraction performance with various document types (PDF, JPEG, TIFF)
- [ ] T249 Benchmark API response times under load (100 concurrent requests)
- [ ] T250 [P] Optimize frontend bundle size and first paint time
- [ ] T251 [P] Add database query caching layer if needed for repeated queries
- [ ] T252 Document performance baselines in backend/docs/performance-baselines.md

### Security Hardening

- [ ] T253 Add CORS configuration to allow only known frontend origins
- [ ] T254 [P] Implement HTTPS redirect in production configuration
- [ ] T255 [P] Add security headers (X-Frame-Options, CSP, etc) in middleware
- [ ] T256 Implement input sanitization for all text fields (prevent SQL injection, XSS)
- [ ] T257 [P] Run security scan: `bandit backend/src/ --recursive`
- [ ] T258 [P] Review dependencies for known vulnerabilities: `safety check`
- [ ] T259 Document security practices in backend/SECURITY.md

### Docker & Deployment

- [ ] T260 [P] Test docker-compose builds cleanly on fresh machine
- [ ] T261 Test all containers start and communicate correctly
- [ ] T262 [P] Create docker-compose.prod.yml for production-like environment
- [ ] T263 Create Dockerfile multi-stage build for minimal production images
- [ ] T264 [P] Add container image versioning strategy (tag with version)
- [ ] T265 Document container deployment in backend/docs/docker.md

### Error Handling & Logging

- [ ] T266 Review all error messages for clarity and actionability
- [ ] T267 [P] Ensure all Celery task failures log with full stack trace
- [ ] T268 [P] Verify all API errors return consistent error response format
- [ ] T269 Implement centralized error tracking (Sentry integration if applicable)
- [ ] T270 [P] Test error scenarios: missing files, database down, Azure API timeout

### Final Validation

- [ ] T271 [P] Run checklist in quickstart.md: setup, upload document, view results, review, approve
- [ ] T272 [P] Test batch upload with 20 documents, verify all process
- [ ] T273 Test all 16 API endpoints manually or with Postman
- [ ] T274 [P] Verify audit logs show all actions
- [ ] T275 [P] Verify API docs at /docs are complete and functional
- [ ] T276 [P] Code review of all critical paths (extraction, scoring, review approval)

### Acceptance & Handoff

- [ ] T277 Update master README with project overview and links to documentation
- [ ] T278 [P] Create DEPLOYMENT.md with cloud deployment instructions
- [ ] T279 [P] Create TROUBLESHOOTING.md with common issues and solutions
- [ ] T280 [P] Hold knowledge transfer session with operations team
- [ ] T281 Document known limitations and technical debt in FUTURE.md
- [ ] T282 Sign-off: Product owner verifies all acceptance scenarios pass

**Checkpoint**: System complete, documented, tested, secured. Ready for pilot deployment.

---

## Summary & Metrics

### By Phase
| Phase | Tasks | Duration | Team | Status |
|-------|-------|----------|------|--------|
| 1: Setup | 15 | 2-3 days | 1 dev | Ready |
| 2: Foundational | 46 | 5-7 days | 3-4 devs | Ready |
| 3: User Story 1 | 36 | 5-7 days | 3-4 devs | Ready |
| 4: User Story 2 | 19 | 3-4 days | 2-3 devs | Ready |
| 5: User Story 3 | 34 | 6-8 days | 4-5 devs | Ready |
| 6: User Story 4 | 25 | 5-6 days | 3-4 devs | Ready |
| 7: User Story 5 | 18 | 4-5 days | 2-3 devs | Ready |
| 8: User Story 6 | 24 | 4-5 days | 2-3 devs | Ready |
| 9: Polish | 48 | 3-4 days | 2-3 devs | Ready |
| **TOTAL** | **265** | **5-8 weeks** | **3-5 concurrent** | **Ready to Start** |

### By Component
| Component | Tasks | Priority |
|-----------|-------|----------|
| Backend API | 118 | P1 |
| Frontend UI | 82 | P1 |
| Database | 24 | P1 |
| Testing | 26 | P2 |
| Documentation | 12 | P2 |
| DevOps/Deployment | 3 | P2 |

### By Story
| Story | Tasks | Dependency |
|-------|-------|-----------|
| US1: Upload & Extract | 37 | None (after Foundation) |
| US2: Confidence Scoring | 11 | US1 |
| US3: Review Dashboard | 34 | US1, US2 |
| US4: Batch Processing | 25 | Parallel with US1-3 |
| US5: REST API | 18 | Parallel with US1-4 |
| US6: Audit Logging | 24 | Parallel with US1-5 |

---

## Execution Strategy: Recommended Team Allocation

### Option 1: Sequential Delivery (MVP First)
```
Sprint 1-2: Phase 1 + Phase 2 (Setup + Foundation)
Sprint 3-4: Phase 3 (User Story 1: Upload & Extract) → MVP ready
Sprint 5: Phase 4 (User Story 2: Confidence Scoring)
Sprint 6: Phase 5 (User Story 3: Review Dashboard) → Core feature complete
Sprint 7+: Parallel on US4/US5/US6
```

### Option 2: Parallel Execution (Faster Time-to-Market)
```
Sprint 1: Phase 1 (Setup)
Sprint 2: Phase 2 (Foundation)
Sprint 3-4: Parallel: US1 + US4 (Extract + Batch), separate backend/frontend teams
Sprint 5: Parallel: US2 (Scoring) + US5 (API) + US6 (Audit)
Sprint 6: US3 (Review Dashboard)
Sprint 7: Polish & Optimization
```

---

## Success Criteria per Task

Each task includes implicit success criteria:
- Code compiles/runs without errors
- Unit tests pass (if test task)
- Integration tests pass (if integration task)
- Follows project structure defined in plan.md
- Includes appropriate logging and error handling
- Documentation updated (README, docstrings)
- Code reviewed and approved by lead
- Acceptance scenario from spec.md verified

---

## How to Use This Task List

1. **Assign tasks** to developers
2. **Mark tasks complete** as they finish (update `- [ ]` to `- [x]`)
3. **Track dependencies** - ensure blocked tasks are unblocked
4. **Monitor phase checkpoints** - validate gate criteria before moving forward
5. **Update story status** when all tasks in a phase complete
6. **Prioritize blockers** - resolve any Phase 2 issues immediately

---

## Next Steps

1. ✅ Specification complete (spec.md)
2. ✅ Implementation plan complete (plan.md)
3. ✅ Design complete (research.md, data-model.md, contracts/)
4. ✅ **Tasks ready** (this file) → **Begin Phase 1 setup**
5. Next: Assign tasks, start Sprint 1


