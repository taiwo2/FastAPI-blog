from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from app.models.user_model import User
from app.schemas.user_schema import Token
from app.database import get_db
from sqlalchemy.orm import Session
from app.config import settings
from app.exceptions import CredentialsException

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against
    
    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password.
    
    Args:
        password: The plain text password to hash
    
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The data to encode in the token
        expires_delta: Optional timedelta for token expiration
    
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticate a user with email and password.
    
    Args:
        db: Database session
        email: User's email
        password: User's password
    
    Returns:
        User: The authenticated user if successful
    
    Raises:
        CredentialsException: If authentication fails
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise CredentialsException("Incorrect email or password")
    if not verify_password(password, user.password):
        raise CredentialsException("Incorrect email or password")
    return user

def get_current_user(token: str, db: Session) -> User:
    """
    Get the current user from a JWT token.
    
    Args:
        token: The JWT token
        db: Database session
    
    Returns:
        User: The authenticated user
    
    Raises:
        CredentialsException: If token is invalid or user not found
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CredentialsException("Invalid token")
    except JWTError:
        raise CredentialsException("Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise CredentialsException("User not found")
    return user