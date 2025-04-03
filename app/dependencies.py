from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session

security = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to extract and validate token from Authorization header.
    """
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication scheme"
        )
    return credentials.credentials

def get_current_user_dependency(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    """
    Dependency to get current authenticated user.
    """
    return get_current_user(token, db)