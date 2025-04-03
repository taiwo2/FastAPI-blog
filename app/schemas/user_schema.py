from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserBase(BaseModel):
    """
    Base schema for user data with common fields.
    """
    email: EmailStr = Field(..., example="user@example.com")

class UserCreate(UserBase):
    """
    Schema for user creation with password validation.
    """
    password: str = Field(..., min_length=8, max_length=100, 
                         example="strongpassword123")
    
    @validator('password')
    def password_complexity(cls, v):
        """
        Validates that password meets complexity requirements.
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

class UserInDB(UserBase):
    """
    Schema for user data stored in database (includes hashed password).
    """
    id: int
    password: str
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str = "bearer"