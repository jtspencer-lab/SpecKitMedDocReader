"""
Pydantic schemas for review-related API requests/responses.
"""

from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewDetailsResponse(BaseModel):
    """Complete review record with extraction details."""
    
    review_id: str
    extraction_result_id: str
    document_id: str
    status: str
    reviewer_id: Optional[str] = None
    feedback: Optional[str] = None
    is_approved: bool
    rejection_reason: Optional[str] = None
    priority: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReviewUpdateRequest(BaseModel):
    """Request to update review record."""
    
    status: Optional[str] = None
    feedback: Optional[str] = None
    is_approved: Optional[bool] = None
    rejection_reason: Optional[str] = None
    corrections: Optional[Dict[str, str]] = Field(
        None,
        description="Field corrections {field_name: new_value}"
    )


class ReviewApprovalRequest(BaseModel):
    """Request to approve extraction."""
    
    feedback: Optional[str] = None
    corrections: Optional[Dict[str, str]] = None


class ReviewRejectionRequest(BaseModel):
    """Request to reject extraction."""
    
    reason: str = Field(..., description="Rejection reason")
    feedback: Optional[str] = None
