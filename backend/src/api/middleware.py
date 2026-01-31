"""
API middleware for request logging, CORS, and error handling.
"""

import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.utils.logging import get_logger


logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log all incoming requests and responses."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Log request/response with timing.
        
        Args:
            request: HTTP request
            call_next: Next middleware/handler
            
        Returns:
            Response: HTTP response
        """
        start_time = time.time()
        request_id = request.headers.get("x-request-id", "unknown")
        
        # Log request
        logger.info(
            "request_started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown",
            }
        )
        
        try:
            response = await call_next(request)
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                "request_error",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration * 1000,
                    "error": str(e),
                }
            )
            raise
        
        # Log response
        duration = time.time() - start_time
        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration * 1000,
            }
        )
        
        response.headers["X-Process-Time"] = str(duration)
        response.headers["X-Request-ID"] = request_id
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Handle and log application errors."""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Catch errors and format responses.
        
        Args:
            request: HTTP request
            call_next: Next middleware/handler
            
        Returns:
            Response: HTTP response
        """
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.exception("unhandled_exception", extra={"path": request.url.path})
            raise
