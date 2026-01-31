"""
SQLAlchemy Base class and database configuration.
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData

# SQLAlchemy declarative base for all models
Base = declarative_base()

# Naming convention for constraints
naming_convention = {
    "ix": "ix_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base.metadata = MetaData(naming_convention=naming_convention)
