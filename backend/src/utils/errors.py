"""
Global error handling and custom exception classes.
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class AppException(Exception):
    """Base application exception."""
    
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class DocumentNotFoundError(AppException):
    """Document not found in database."""
    
    def __init__(self, document_id: str):
        super().__init__(
            message=f"Document {document_id} not found",
            error_code="DOCUMENT_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"document_id": document_id},
        )


class ExtractionNotFoundError(AppException):
    """Extraction result not found."""
    
    def __init__(self, extraction_id: str):
        super().__init__(
            message=f"Extraction {extraction_id} not found",
            error_code="EXTRACTION_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"extraction_id": extraction_id},
        )


class InvalidDocumentError(AppException):
    """Invalid or corrupted document."""
    
    def __init__(self, reason: str):
        super().__init__(
            message=f"Invalid document: {reason}",
            error_code="INVALID_DOCUMENT",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"reason": reason},
        )


class FileTooLargeError(AppException):
    """Uploaded file exceeds maximum size."""
    
    def __init__(self, file_size: int, max_size: int):
        super().__init__(
            message=f"File size {file_size} exceeds maximum {max_size}",
            error_code="FILE_TOO_LARGE",
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            details={"file_size": file_size, "max_size": max_size},
        )


class ProcessingError(AppException):
    """Error during document processing."""
    
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"Processing error: {message}",
            error_code="PROCESSING_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details or {},
        )


def app_exception_handler(exc: AppException) -> HTTPException:
    """Convert app exception to HTTP exception."""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        }
    )
