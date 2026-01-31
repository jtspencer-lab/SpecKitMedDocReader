"""
Audit log model for tracking all system changes (HIPAA compliance).
"""

from enum import Enum
from sqlalchemy import Column, String, Text, Integer, Index
from sqlalchemy.dialects.postgresql import JSON
from src.db.base import Base
from src.models.common import AuditMixin


class AuditActionType(str, Enum):
    """Type of auditable action."""
    DOCUMENT_UPLOAD = "document_upload"
    EXTRACTION_START = "extraction_start"
    EXTRACTION_COMPLETE = "extraction_complete"
    FIELD_EXTRACTED = "field_extracted"
    FIELD_CORRECTED = "field_corrected"
    REVIEW_STARTED = "review_started"
    REVIEW_APPROVED = "review_approved"
    REVIEW_REJECTED = "review_rejected"
    BATCH_STARTED = "batch_started"
    BATCH_COMPLETED = "batch_completed"
    DATA_ACCESSED = "data_accessed"
    DATA_EXPORTED = "data_exported"


class AuditLog(Base):
    """
    Immutable audit log for compliance and accountability.
    
    Attributes:
        id: Unique audit log entry ID
        action_type: Type of action taken
        actor_id: User/system performing action
        resource_type: Type of resource affected (Document, ExtractionResult, etc.)
        resource_id: ID of affected resource
        old_value: Previous value (for corrections)
        new_value: New value
        details: Additional action details as JSON
        ip_address: IP address of actor
        user_agent: User agent string if web request
        created_at: Timestamp of action (immutable)
    
    This table is append-only for compliance and cannot be modified after creation.
    """
    
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, index=True)
    action_type = Column(String(50), nullable=False, index=True)
    actor_id = Column(String(255), nullable=True, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(String(255), nullable=True, index=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(AuditMixin.created_at.type, nullable=False, index=True)
    
    # Composite indices for common queries
    __table_args__ = (
        Index('ix_audit_resource', 'resource_type', 'resource_id'),
        Index('ix_audit_actor_date', 'actor_id', 'created_at'),
    )
    
    def __repr__(self) -> str:
        return f"<AuditLog {self.action_type} on {self.resource_type}/{self.resource_id}>"
