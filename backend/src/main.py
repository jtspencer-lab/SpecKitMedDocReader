"""
FastAPI application entry point.

Initializes the FastAPI application with middleware, exception handlers,
startup/shutdown events, and route registration.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.utils.logging import setup_logging
from src.utils.errors import AppException, app_exception_handler
from src.api.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware


logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown events.
    
    Startup: Initialize database connections, load models, etc.
    Shutdown: Clean up resources.
    """
    # Startup
    logger.info(f"Starting application in {settings.environment} environment")
    logger.info(f"Database URL: {settings.database_url}")
    logger.info(f"Redis URL: {settings.redis_url}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    # Setup logging
    setup_logging(settings.log_level)
    
    # Create app
    app = FastAPI(
        title="Document Extraction & Analysis API",
        description="Automated document processing system for patient/signup information extraction",
        version="0.1.0",
        lifespan=lifespan,
    )
    
    # Add middleware - CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add middleware - Trusted Host
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "*.example.com"],
    )
    
    # Add middleware - Error handling and logging
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    
    # Exception handlers
    @app.exception_handler(AppException)
    async def custom_exception_handler(request, exc: AppException):
        """Handle custom application exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc: RequestValidationError):
        """Handle validation errors."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            },
        )
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint for monitoring and load balancers."""
        return {
            "status": "healthy",
            "environment": settings.environment,
            "version": "0.1.0",
        }
    
    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information."""
        return {
            "name": "Document Extraction & Analysis API",
            "version": "0.1.0",
            "docs": "/docs",
            "openapi": "/openapi.json",
        }
    
    # TODO: Register route modules
    # from src.api.routes import documents, reviews, batch, audit
    # app.include_router(documents.router)
    # app.include_router(reviews.router)
    # app.include_router(batch.router)
    # app.include_router(audit.router)
    
    logger.info("Application initialized successfully")
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower(),
    )
