"""
Document model for storing uploaded medical documents.
"""

from enum import Enum
from sqlalchemy import Column, String, Integer, Float, Enum as SQLEnum, Text, LargeBinary
from sqlalchemy.orm import relationship
from src.db.base import Base
from src.models.common import AuditMixin


class DocumentStatus(str, Enum):
    """Document processing status."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class DocumentType(str, Enum):
    """Type of medical document."""
    PATIENT_FORM = "patient_form"
    INSURANCE = "insurance"
    MEDICAL_RECORD = "medical_record"
    LAB_REPORT = "lab_report"
    SCAN = "scan"
    OTHER = "other"


class Document(Base, AuditMixin):
    """
    Represents an uploaded medical document.
    
    Attributes:
        id: Unique document identifier (UUID)
        filename: Original uploaded filename
        file_size: File size in bytes
        document_type: Type of document
        status: Current processing status
        mime_type: MIME type of file (pdf, image/png, etc.)
        patient_id: Associated patient ID (optional)
        confidence_score: Overall confidence score (0-1)
        extraction_attempts: Number of extraction attempts
        last_error: Last error message if processing failed
        notes: Additional notes or metadata
        created_at: Timestamp of upload
        updated_at: Timestamp of last status change
    """
    
    __tablename__ = "documents"
    
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)  # bytes
    document_type = Column(SQLEnum(DocumentType), nullable=False, default=DocumentType.OTHER)
    status = Column(SQLEnum(DocumentStatus), nullable=False, default=DocumentStatus.UPLOADED)
    mime_type = Column(String(50), nullable=False)
    patient_id = Column(String(100), nullable=True, index=True)
    confidence_score = Column(Float, nullable=True)  # 0-1
    extraction_attempts = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships (defined when other models are created)
    # extraction_results = relationship("ExtractionResult", back_populates="document")
    
    def __repr__(self) -> str:
        return f"<Document {self.id} ({self.filename})>"
