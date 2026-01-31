"""Database initialization for testing."""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from src.db.base import Base


def init_test_db(database_url: str = "sqlite:///:memory:") -> Session:
    """
    Initialize test database with schema.
    
    Args:
        database_url: SQLite in-memory database URL
        
    Returns:
        Session: Test database session
    """
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def clear_test_db(session: Session) -> None:
    """
    Clear all tables from test database.
    
    Args:
        session: Database session
    """
    Base.metadata.drop_all(bind=session.get_bind())


def seed_test_data(session: Session) -> None:
    """
    Seed test database with sample data.
    
    Args:
        session: Database session
    """
    # Placeholder for test data seeding
    # Will be populated as models are created
    pass
