"""
Pydantic schemas for extraction-related API requests/responses.
"""

from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel, Field


class ExtractionFieldData(BaseModel):
    """Single extracted field."""
    
    field_name: str = Field(..., description="Field name (first_name, dob, etc.)")
    field_value: str = Field(..., description="Extracted value")
    confidence: float = Field(..., ge=0, le=1, description="Confidence 0-1")
    confidence_source: str = Field(..., description="How confidence was calculated")
    
    class Config:
        from_attributes = True


class ExtractionResultResponse(BaseModel):
    """Complete extraction result response."""
    
    id: str
    document_id: str
    status: str
    overall_confidence: float = Field(..., ge=0, le=1)
    is_flagged: bool
    flag_reason: Optional[str] = None
    fields: List[ExtractionFieldData] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ExtractionResultDetailResponse(ExtractionResultResponse):
    """Detailed extraction with raw OCR text."""
    
    raw_ocr_text: Optional[str] = None
    ocr_confidence: Optional[float] = None
    nlp_confidence: Optional[float] = None
    extracted_data: Optional[Dict] = None
