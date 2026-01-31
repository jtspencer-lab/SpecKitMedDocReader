"""
Extraction result models for storing OCR and NLP output.
"""

from enum import Enum
from sqlalchemy import Column, String, Integer, Float, Enum as SQLEnum, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from src.db.base import Base
from src.models.common import AuditMixin


class FieldConfidenceSource(str, Enum):
    """Source of confidence score for extracted field."""
    OCR = "ocr"
    NLP = "nlp"
    VALIDATION = "validation"
    COMPOSITE = "composite"


class ExtractionResult(Base, AuditMixin):
    """
    Represents complete extraction result for a document.
    
    Attributes:
        id: Unique result identifier
        document_id: Reference to Document
        status: Extraction status (complete, partial, failed)
        ocr_confidence: Raw OCR confidence (0-1)
        nlp_confidence: NLP entity extraction confidence (0-1)
        overall_confidence: Combined confidence score (0-1)
        is_flagged: Whether result was flagged for review
        flag_reason: Reason for flagging (confidence below threshold, etc.)
        extracted_data: JSON with all extracted fields
        raw_ocr_text: Raw OCR output before processing
    """
    
    __tablename__ = "extraction_results"
    
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="complete")  # complete, partial, failed
    ocr_confidence = Column(Float, nullable=True)  # 0-1
    nlp_confidence = Column(Float, nullable=True)  # 0-1
    overall_confidence = Column(Float, nullable=False)  # 0-1
    is_flagged = Column(Boolean, default=False, index=True)
    flag_reason = Column(String(255), nullable=True)
    extracted_data = Column(JSON, nullable=True)  # Store all fields as JSON
    raw_ocr_text = Column(Text, nullable=True)
    
    # Relationships
    # fields = relationship("ExtractionField", back_populates="extraction_result")
    
    def __repr__(self) -> str:
        return f"<ExtractionResult {self.id} (confidence: {self.overall_confidence})>"


class ExtractionField(Base, AuditMixin):
    """
    Represents an individual extracted field from a document.
    
    Attributes:
        id: Unique field identifier
        extraction_result_id: Reference to ExtractionResult
        field_name: Name of extracted field (first_name, dob, etc.)
        field_value: Extracted value
        confidence: Field-specific confidence (0-1)
        confidence_source: How confidence was calculated
        validator_feedback: Human reviewer corrections/feedback
    """
    
    __tablename__ = "extraction_fields"
    
    extraction_result_id = Column(String(36), ForeignKey("extraction_results.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    field_value = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)  # 0-1
    confidence_source = Column(SQLEnum(FieldConfidenceSource), nullable=False)
    validator_feedback = Column(Text, nullable=True)
    
    # Index for common queries
    __table_args__ = (
        ('ix_field_name_result', 'extraction_result_id', 'field_name'),
    )
    
    def __repr__(self) -> str:
        return f"<ExtractionField {self.field_name}={self.field_value}>"
