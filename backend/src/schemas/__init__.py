"""
Schemas package - Pydantic models for API requests/responses.

This module exports all schemas for API documentation and request validation.
"""

from src.schemas.document import (
    DocumentUploadResponse,
    DocumentResponse,
    DocumentStatusResponse,
)
from src.schemas.extraction import (
    ExtractionFieldData,
    ExtractionResultResponse,
    ExtractionResultDetailResponse,
)
from src.schemas.review import (
    ReviewDetailsResponse,
    ReviewUpdateRequest,
    ReviewApprovalRequest,
    ReviewRejectionRequest,
)


__all__ = [
    # Document schemas
    "DocumentUploadResponse",
    "DocumentResponse",
    "DocumentStatusResponse",
    # Extraction schemas
    "ExtractionFieldData",
    "ExtractionResultResponse",
    "ExtractionResultDetailResponse",
    # Review schemas
    "ReviewDetailsResponse",
    "ReviewUpdateRequest",
    "ReviewApprovalRequest",
    "ReviewRejectionRequest",
]
