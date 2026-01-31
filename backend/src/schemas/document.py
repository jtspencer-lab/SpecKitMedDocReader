"""
Pydantic schemas for document-related API requests/responses.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    """Response after successful document upload."""
    
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Uploaded filename")
    file_size: int = Field(..., description="File size in bytes")
    status: str = Field(default="uploaded", description="Processing status")
    created_at: datetime = Field(..., description="Upload timestamp")
    
    class Config:
        from_attributes = True


class DocumentResponse(BaseModel):
    """Full document information response."""
    
    id: str
    filename: str
    file_size: int
    document_type: str
    status: str
    mime_type: str
    confidence_score: Optional[float] = None
    extraction_attempts: int
    patient_id: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentStatusResponse(BaseModel):
    """Document processing status response."""
    
    document_id: str
    status: str
    confidence_score: Optional[float] = None
    extraction_attempts: int
    last_error: Optional[str] = None
    updated_at: datetime
    
    class Config:
        from_attributes = True
