"""
Dependency injection for FastAPI routes.

Provides common dependencies like database sessions, authentication, etc.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.session import SessionLocal


async def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency for API routes.
    
    Yields:
        Session: SQLAlchemy database session
        
    Raises:
        HTTPException: If database connection fails
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    finally:
        db.close()


async def get_current_user(token: str = None) -> dict:
    """
    Get current authenticated user from token.
    
    Args:
        token: Bearer token from Authorization header
        
    Returns:
        dict: User information
        
    Raises:
        HTTPException: If token is invalid or missing
        
    Note: This is a placeholder. Implement JWT verification logic.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # TODO: Verify JWT token and extract user info
    # return jwt.decode(token, settings.secret_key)
    
    return {"user_id": "user-1", "email": "user@example.com"}
