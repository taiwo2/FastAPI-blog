from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class User(Base):
    """
    SQLAlchemy model representing a user in the system.
    
    Attributes:
        id (int): Primary key
        email (str): User's email address (unique)
        password (str): Hashed password
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)