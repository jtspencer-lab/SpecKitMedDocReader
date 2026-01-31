"""
Database session management and connection configuration.
"""

from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool, QueuePool

from src.config import get_settings


settings = get_settings()


def create_db_engine():
    """
    Create database engine with connection pooling.
    
    Returns:
        Engine: SQLAlchemy engine instance
    """
    # Use NullPool for SQLite (testing), QueuePool for PostgreSQL
    if "sqlite" in settings.database_url:
        poolclass = NullPool
        kwargs = {}
    else:
        poolclass = QueuePool
        kwargs = {
            "pool_size": settings.database_pool_size,
            "max_overflow": settings.database_max_overflow,
            "pool_pre_ping": True,  # Test connections before using
            "pool_recycle": 3600,   # Recycle connections after 1 hour
        }
    
    engine = create_engine(
        settings.database_url,
        echo=settings.database_echo,
        poolclass=poolclass,
        **kwargs
    )
    
    # Enable foreign keys for SQLite
    if "sqlite" in settings.database_url:
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
    
    return engine


engine = create_db_engine()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection for database session.
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_sync() -> Session:
    """
    Get synchronous database session (for non-async contexts).
    
    Returns:
        Session: Database session
    """
    return SessionLocal()
