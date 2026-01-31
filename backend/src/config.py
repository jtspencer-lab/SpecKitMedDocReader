"""
Application configuration management.

Provides environment-based configuration for development, testing, and production.
Uses Pydantic for validation and type safety.
"""

from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Environment
    environment: str = "development"
    debug: bool = False
    
    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # Database
    database_url: str = "postgresql://signupreader:password@localhost:5432/signupreader_db"
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 10
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"
    celery_task_time_limit: int = 3600
    celery_task_soft_time_limit: int = 3300
    
    # Azure Form Recognizer
    azure_form_recognizer_endpoint: str = ""
    azure_form_recognizer_key: str = ""
    
    # JWT/Auth
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # File Upload
    upload_dir: str = "./uploads"
    max_file_size: int = 52428800  # 50MB
    allowed_extensions: list[str] = ["pdf", "png", "jpg", "jpeg", "tiff"]
    
    # OCR Settings
    ocr_confidence_threshold: float = 0.8
    ocr_language: str = "en"
    
    # NLP Settings
    spacy_model: str = "en_core_web_md"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    log_file: Optional[str] = None
    
    # Audit
    enable_audit_logging: bool = True
    audit_log_retention_days: int = 365
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()


def get_environment() -> str:
    """Get current environment."""
    return get_settings().environment


def is_development() -> bool:
    """Check if running in development mode."""
    return get_settings().environment == "development"


def is_production() -> bool:
    """Check if running in production mode."""
    return get_settings().environment == "production"
