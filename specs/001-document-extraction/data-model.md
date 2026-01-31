# Data Model: Document Extraction & Analysis System

**Created**: January 19, 2026  
**Phase**: Phase 1 - Design  
**Purpose**: Define all entities, relationships, validation rules, and database schema

## Entity Relationship Diagram

```
┌──────────────┐
│  Document    │ 1 --- N
├──────────────┤       │
│ id (PK)      │       │
│ filename     │       │ ┌─────────────────────┐
│ file_size    │       └─┤ ExtractionResult    │ 1 --- N
│ upload_date  │       1 ├─────────────────────┤
│ format       │         │ id (PK)             │
│ status       │         │ document_id (FK)    │
│ user_id      │         │ created_at          │
└──────────────┘         │ overall_confidence  │
       │                 │ extraction_data     │ (JSON)
       │                 └─────────────────────┘
       │                         │
       │                         N
       │                         │
       │                  ┌──────────────────┐
       │                  │ ExtractionField  │
       │                  ├──────────────────┤
       │                  │ id (PK)          │
       │                  │ extraction_id    │ (FK)
       │                  │ field_name       │
       │                  │ field_value      │
       │                  │ confidence       │
       │                  │ flagged_for_review
       │                  └──────────────────┘
       │
       N
       │
       └──────────────────┬──────────────────────┐
                          │                      │
                    ┌─────▼────────┐    ┌───────▼──────┐
                    │ ReviewRecord │ 1-N│  AuditLog    │
                    ├──────────────┤    ├──────────────┤
                    │ id (PK)      │    │ id (PK)      │
                    │ document_id  │ FK │ timestamp    │
                    │ reviewer_id  │    │ user_id      │
                    │ review_date  │    │ action       │
                    │ status       │    │ entity_type  │
                    │ comments     │    │ entity_id    │
                    │ changes      │    │ change_data  │
                    │ (JSON array) │    │ (JSON)       │
                    └──────────────┘    └──────────────┘


Also linked to Patient entity:
    
    ┌──────────────┐
    │   Patient    │
    ├──────────────┤
    │ id (PK)      │
    │ name         │
    │ dob          │
    │ gender       │
    │ contact_info │
    │ insurance    │
    │ created_from_doc_id (FK to Document)
    └──────────────┘
```

---

## Core Entities

### 1. Document

Represents an uploaded medical document file.

```python
# Pydantic Model (request/response)
class DocumentMetadata(BaseModel):
    filename: str                    # Original filename (e.g., "patient_form_2026-01-19.pdf")
    file_size: int                   # Size in bytes
    format: str                      # "pdf", "jpeg", "png", "tiff"
    mime_type: str                   # "application/pdf", "image/jpeg", etc.
    
class DocumentResponse(DocumentMetadata):
    id: UUID
    user_id: UUID                    # User who uploaded
    upload_date: datetime
    processing_status: str           # "pending", "processing", "completed", "failed"
    error_message: Optional[str]     # If status == "failed"
    processing_started_at: Optional[datetime]
    processing_completed_at: Optional[datetime]
    extraction_result_id: Optional[UUID]  # Link to extraction once ready


# SQLAlchemy ORM Model (database table)
class Document(Base):
    __tablename__ = "documents"
    
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    filename: str = Column(String(255), nullable=False)
    file_size: int = Column(Integer, nullable=False)
    format: str = Column(String(10), nullable=False)  # Enum in DB
    mime_type: str = Column(String(50))
    user_id: UUID = Column(UUID, nullable=False)  # Audit trail
    upload_date: datetime = Column(DateTime, default=datetime.utcnow)
    processing_status: str = Column(String(20), default="pending")
    error_message: Optional[str] = Column(String(1000))
    processing_started_at: Optional[datetime] = Column(DateTime)
    processing_completed_at: Optional[datetime] = Column(DateTime)
    extraction_result_id: Optional[UUID] = Column(UUID)
    
    # Relationships
    extraction_results = relationship("ExtractionResult", back_populates="document")
    review_records = relationship("ReviewRecord", back_populates="document")
    audit_logs = relationship("AuditLog", back_populates="entity")
    
    # Indexes
    __table_args__ = (
        Index('idx_document_status', 'processing_status'),
        Index('idx_document_user_date', 'user_id', 'upload_date'),
    )
```

**Validation Rules**:
- `filename`: Required, max 255 chars, must contain file extension
- `file_size`: Must be 100KB - 50MB
- `format`: Must be one of: pdf, jpeg, png, tiff
- `user_id`: Must reference existing user

---

### 2. ExtractionResult

Contains the complete extraction output for a single document.

```python
class ExtractionFieldData(BaseModel):
    field_name: str              # e.g., "patient_name", "date_of_birth", "insurance_id"
    field_value: str             # Extracted value
    confidence: float            # 0.0-1.0 confidence score
    flagged_for_review: bool     # True if confidence < 0.8
    source: str                  # "azure_form_recognizer", "spacy_nlp", "manual"
    metadata: Optional[dict]     # OCR region coordinates, entity type, etc.

class ExtractionResultResponse(BaseModel):
    id: UUID
    document_id: UUID
    overall_confidence: float    # Average of all field confidences
    created_at: datetime
    fields: List[ExtractionFieldData]
    flagged_count: int          # Number of fields flagged for review
    raw_azure_response: dict    # Store original API response for audit
    processing_time_ms: int     # For monitoring


class ExtractionResult(Base):
    __tablename__ = "extraction_results"
    
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    document_id: UUID = Column(UUID, ForeignKey("documents.id"), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    overall_confidence: float = Column(Float)
    extraction_data: dict = Column(JSON)  # Full structured extraction
    raw_azure_response: dict = Column(JSON)  # Audit trail
    processing_time_ms: int = Column(Integer)
    
    # Relationships
    document = relationship("Document", back_populates="extraction_results")
    fields = relationship("ExtractionField", back_populates="extraction_result")
    review_record = relationship("ReviewRecord", uselist=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_extraction_document', 'document_id'),
        Index('idx_extraction_created', 'created_at'),
    )
```

**Validation Rules**:
- `overall_confidence`: Must be 0.0-1.0
- `extraction_data`: Must be valid JSON with required keys
- All extraction fields must have valid values or be explicitly null

---

### 3. ExtractionField

Individual extracted field (one per extracted data point).

```python
class ExtractionFieldData(BaseModel):
    field_name: str              # "patient_name", "dob", "insurance_id", etc.
    field_value: str
    confidence: float            # 0.0-1.0
    flagged_for_review: bool     # True if confidence < 0.8
    source: str                  # "azure", "spacy", "pattern", "manual"
    
class ExtractionField(Base):
    __tablename__ = "extraction_fields"
    
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    extraction_result_id: UUID = Column(UUID, ForeignKey("extraction_results.id"))
    field_name: str = Column(String(100), nullable=False)
    field_value: str = Column(String(500))
    confidence: float = Column(Float, nullable=False)
    flagged_for_review: bool = Column(Boolean, default=False)
    source: str = Column(String(50))  # azure, spacy, pattern, manual
    
    # Relationships
    extraction_result = relationship("ExtractionResult", back_populates="fields")
    
    # Indexes
    __table_args__ = (
        Index('idx_extraction_field_name', 'field_name'),
        Index('idx_extraction_flagged', 'flagged_for_review'),
    )
```

**Confidence Scoring Algorithm** (from research.md):
```python
def calculate_field_confidence(
    azure_score: float,      # Form Recognizer confidence
    ocr_quality: float,      # 0-1 based on document clarity
    nlp_confidence: float,   # spaCy entity confidence
    validation_score: float  # Format/pattern match score
) -> float:
    return (
        0.5 * azure_score +
        0.2 * ocr_quality +
        0.2 * nlp_confidence +
        0.1 * validation_score
    )
```

---

### 4. ReviewRecord

Tracks human review of a document's extraction results.

```python
class ReviewChange(BaseModel):
    field_name: str
    old_value: Optional[str]
    new_value: str
    timestamp: datetime
    reviewer_id: UUID

class ReviewRecordResponse(BaseModel):
    id: UUID
    document_id: UUID
    reviewer_id: UUID
    review_date: datetime
    review_status: str          # "pending", "in_progress", "approved", "rejected"
    approval_status: Optional[str]  # "approved", "rejected"
    rejection_reason: Optional[str] # If rejected
    changes: List[ReviewChange]     # All edits made
    comments: Optional[str]         # Reviewer notes
    completed_at: Optional[datetime]


class ReviewRecord(Base):
    __tablename__ = "review_records"
    
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    document_id: UUID = Column(UUID, ForeignKey("documents.id"), nullable=False)
    extraction_result_id: UUID = Column(UUID, ForeignKey("extraction_results.id"))
    reviewer_id: UUID = Column(UUID, nullable=False)  # User who reviewed
    review_date: datetime = Column(DateTime, default=datetime.utcnow)
    review_status: str = Column(String(20), default="pending")  # pending, in_progress, completed
    approval_status: str = Column(String(20))  # approved, rejected, null
    rejection_reason: Optional[str] = Column(String(500))
    changes: dict = Column(JSON)  # List of ReviewChange objects
    comments: Optional[str] = Column(String(2000))
    completed_at: Optional[datetime] = Column(DateTime)
    
    # Relationships
    document = relationship("Document", back_populates="review_records")
    
    # Indexes
    __table_args__ = (
        Index('idx_review_status', 'review_status'),
        Index('idx_review_reviewer_date', 'reviewer_id', 'review_date'),
    )
```

**Workflow States**:
- `review_status: "pending"` → Document flagged, awaiting reviewer
- `review_status: "in_progress"` → Reviewer opened record, not yet saved changes
- `review_status: "completed"` → Reviewer finished; `approval_status` indicates outcome

**Change Tracking**:
- Every field edit is recorded in `changes` array
- Includes timestamp, reviewer_id, old_value, new_value
- Enables full audit trail and rollback capability

---

### 5. AuditLog

Immutable log of all system activities for compliance.

```python
class AuditLogEntry(BaseModel):
    timestamp: datetime
    user_id: UUID
    action: str                 # "document_uploaded", "extraction_completed", "review_approved", etc.
    entity_type: str            # "document", "extraction_result", "review_record"
    entity_id: UUID
    change_data: dict           # What changed (before/after, field names, etc.)
    ip_address: Optional[str]
    status: str                 # "success", "failure"
    error_message: Optional[str]


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    timestamp: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id: UUID = Column(UUID, nullable=False)
    action: str = Column(String(50), nullable=False)
    entity_type: str = Column(String(50), nullable=False)
    entity_id: UUID = Column(UUID, nullable=False)
    change_data: dict = Column(JSON)
    ip_address: Optional[str] = Column(String(45))  # IPv4 or IPv6
    status: str = Column(String(20), default="success")
    error_message: Optional[str] = Column(String(500))
    
    # Indexes for querying
    __table_args__ = (
        Index('idx_audit_timestamp', 'timestamp'),
        Index('idx_audit_user_action', 'user_id', 'action'),
        Index('idx_audit_entity', 'entity_type', 'entity_id'),
        Index('idx_audit_action', 'action'),
    )
```

**Immutability**: AuditLog is write-only. Never update or delete audit records.

**Actions Logged**:
- `document_uploaded`
- `extraction_started`
- `extraction_completed`
- `extraction_failed`
- `review_started`
- `review_field_edited`
- `review_approved`
- `review_rejected`
- `result_exported`

---

### 6. Patient

Extracted patient/signup entity from documents.

```python
class ContactInfo(BaseModel):
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip_code: Optional[str]

class PatientResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Optional[str]  # "M", "F", "Other", null
    ssn: Optional[str]     # Last 4 only (privacy)
    contact_info: ContactInfo
    insurance_info: dict   # {provider, member_id, group_id, etc.}
    emergency_contacts: List[dict]
    medical_history: List[str]
    allergies: List[str]
    medications: List[str]
    created_from_document_id: UUID  # Audit trail
    confidence_scores: dict  # {field: confidence_score}


class Patient(Base):
    __tablename__ = "patients"
    
    id: UUID = Column(UUID, primary_key=True, default=uuid4)
    first_name: str = Column(String(100), nullable=False)
    last_name: str = Column(String(100), nullable=False)
    date_of_birth: date = Column(Date, nullable=False)
    gender: Optional[str] = Column(String(10))
    ssn_last_four: Optional[str] = Column(String(4))  # Privacy: only last 4
    phone: Optional[str] = Column(String(20))
    email: Optional[str] = Column(String(255))
    address: Optional[str] = Column(String(255))
    city: Optional[str] = Column(String(100))
    state: Optional[str] = Column(String(2))
    zip_code: Optional[str] = Column(String(10))
    
    # Insurance
    insurance_provider: Optional[str] = Column(String(100))
    insurance_member_id: Optional[str] = Column(String(50))
    insurance_group_id: Optional[str] = Column(String(50))
    
    # Medical
    medical_history: dict = Column(JSON)  # List of conditions/procedures
    allergies: dict = Column(JSON)        # List of allergies
    medications: dict = Column(JSON)      # List of current medications
    emergency_contacts: dict = Column(JSON)
    
    # Audit
    created_from_document_id: UUID = Column(UUID, ForeignKey("documents.id"))
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_at: datetime = Column(DateTime, onupdate=datetime.utcnow)
    confidence_scores: dict = Column(JSON)  # {field_name: score}
    
    # Indexes
    __table_args__ = (
        Index('idx_patient_name', 'first_name', 'last_name'),
        Index('idx_patient_dob', 'date_of_birth'),
        Index('idx_patient_ssn', 'ssn_last_four'),
    )
```

**Privacy Considerations**:
- Full SSN never stored (only last 4 digits for matching)
- PII encrypted at database column level
- Separate access logs for patient record access
- HIPAA de-identification rules enforced

---

## Validation Rules Summary

| Entity | Field | Validation |
|--------|-------|-----------|
| Document | filename | Required, max 255 chars, valid extension |
| | file_size | 100KB - 50MB |
| | format | enum: pdf, jpeg, png, tiff |
| ExtractionField | confidence | 0.0-1.0 |
| | field_value | Non-empty if confidence > 0.5 |
| ReviewRecord | reviewer_id | Must reference existing user |
| Patient | first_name, last_name | Required, max 100 chars |
| | date_of_birth | Valid date, age > 0 |
| | email | Valid email format |
| | ssn_last_four | Exactly 4 digits |
| AuditLog | action | Predefined enum |
| | user_id | Must reference existing user |

---

## Database Indexes

Critical indexes for query performance:

```sql
-- Query by document processing status
CREATE INDEX idx_document_status ON documents(processing_status);

-- Query documents by user and date
CREATE INDEX idx_document_user_date ON documents(user_id, upload_date DESC);

-- Find flagged extraction fields
CREATE INDEX idx_extraction_flagged ON extraction_fields(flagged_for_review, confidence);

-- Query audit log by date range (for compliance reports)
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp DESC);

-- Query audit log by user action (who did what)
CREATE INDEX idx_audit_user_action ON audit_logs(user_id, action, timestamp DESC);

-- Query review records pending
CREATE INDEX idx_review_status ON review_records(review_status, review_date);

-- Patient searches by name
CREATE INDEX idx_patient_name ON patients(first_name, last_name);
```

---

## Migration Strategy

Using Alembic for database migrations:

1. Initial migration creates all tables
2. Migrations versioned with timestamps
3. All migrations reversible (can rollback)
4. Migrations run automatically on deployment

Example migration:
```python
# migrations/versions/001_initial_schema.py
def upgrade():
    op.create_table('documents', ...)
    op.create_table('extraction_results', ...)
    # ... all tables

def downgrade():
    op.drop_table('documents')
    # ... reverse order
```

---

## Next Steps

1. Generate OpenAPI contracts from these models
2. Create SQLAlchemy session management
3. Write unit tests for model validation
4. Set up database locally with test fixtures
