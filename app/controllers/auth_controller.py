from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.user_schema import UserCreate, Token
from app.services.auth_service import (
    get_current_user,
    authenticate_user,
    create_access_token,
    get_password_hash
)
from app.database import get_db
from app.models.user_model import User
from app.config import settings

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.
    
    Args:
        user_data: User registration data (email and password)
        db: Database session dependency
    
    Returns:
        Token: JWT access token for the new user
    
    Raises:
        HTTPException: If email is already registered
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(email=user_data.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    
    Args:
        form_data: OAuth2 password form data (username=email, password)
        db: Database session dependency
    
    Returns:
        Token: JWT access token
    
    Raises:
        HTTPException: If authentication fails
    """
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}