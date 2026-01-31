"""
Review record model for tracking human review of extractions.
"""

from enum import Enum
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from src.db.base import Base
from src.models.common import AuditMixin


class ReviewStatus(str, Enum):
    """Status of review workflow."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CORRECTION = "needs_correction"


class ReviewRecord(Base, AuditMixin):
    """
    Represents human review of an extraction result.
    
    Attributes:
        id: Unique review identifier
        extraction_result_id: Reference to ExtractionResult being reviewed
        status: Current review status
        reviewer_id: ID of reviewer (email or user ID)
        corrections: JSON with field corrections
        feedback: Reviewer's notes/comments
        is_approved: Whether extraction was approved
        rejection_reason: Reason for rejection if rejected
    """
    
    __tablename__ = "review_records"
    
    extraction_result_id = Column(String(36), ForeignKey("extraction_results.id"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default=ReviewStatus.PENDING)
    reviewer_id = Column(String(255), nullable=True, index=True)
    corrections = Column(JSON, nullable=True)  # Field corrections {field_name: new_value}
    feedback = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False, index=True)
    rejection_reason = Column(Text, nullable=True)
    priority = Column(Integer, default=0)  # Priority for review queue
    
    def __repr__(self) -> str:
        return f"<ReviewRecord {self.id} (status: {self.status})>"
