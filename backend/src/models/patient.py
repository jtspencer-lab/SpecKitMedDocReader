"""
Patient model for storing patient/signup information.
"""

from sqlalchemy import Column, String, Date, Text
from src.db.base import Base
from src.models.common import AuditMixin


class Patient(Base, AuditMixin):
    """
    Represents a patient or signup subject.
    
    This is a simplified model. For HIPAA compliance:
    - SSN is stored as last-4-digits only
    - Full details would be stored in encrypted column
    - PII fields should be encrypted at-rest
    
    Attributes:
        id: Unique patient identifier (UUID)
        external_id: External system patient ID
        first_name: Patient first name
        last_name: Patient last name
        date_of_birth: Patient DOB
        ssn_last_four: Last 4 digits of SSN (for display only)
        email: Contact email
        phone: Contact phone number
        address: Street address
        notes: Additional patient notes
    """
    
    __tablename__ = "patients"
    
    external_id = Column(String(100), nullable=True, unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    ssn_last_four = Column(String(4), nullable=True)  # For display only
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<Patient {self.first_name} {self.last_name}>"
