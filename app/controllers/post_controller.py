from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.schemas.post_schema import PostCreate, PostResponse
from app.services.auth_service import get_current_user
from app.services.post_service import PostService
from app.services.cache_service import CacheService
from app.database import get_db
from app.models.user_model import User
from app.exceptions import CredentialsException, NotFoundException

router = APIRouter()
security = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Extract token from Authorization header.
    
    Args:
        credentials: HTTP authorization credentials
    
    Returns:
        str: Extracted token
    
    Raises:
        CredentialsException: If token is missing or invalid
    """
    if credentials.scheme != "Bearer":
        raise CredentialsException("Invalid authentication scheme")
    return credentials.credentials

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def add_post(
    post_data: PostCreate,
    request: Request,
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    """
    Create a new blog post.
    
    Args:
        post_data: Post content data
        request: FastAPI request object (for size validation)
        token: JWT token for authentication
        db: Database session dependency
    
    Returns:
        PostResponse: The created post
    
    Raises:
        HTTPException: If payload is too large or other errors occur
    """
    # Check payload size (1 MB limit)
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 1024 * 1024:  # 1 MB
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Payload too large (max 1MB)"
        )
    
    try:
        # Authenticate user
        user = get_current_user(token, db)
        
        # Create post
        cache_service = CacheService()
        post_service = PostService(db, cache_service)
        post = post_service.create_post(post_data, user.id)
        
        # Prepare response
        return PostResponse(
            id=post.id,
            text=post.text,
            user_id=post.user_id,
            user_email=user.email
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/posts", response_model=list[PostResponse])
def get_posts(
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    """
    Get all posts for the authenticated user.
    
    Args:
        token: JWT token for authentication
        db: Database session dependency
    
    Returns:
        List[PostResponse]: List of user's posts
    
    Raises:
        HTTPException: If authentication fails or other errors occur
    """
    try:
        # Authenticate user
        user = get_current_user(token, db)
        
        # Get posts
        cache_service = CacheService()
        post_service = PostService(db, cache_service)
        posts = post_service.get_user_posts(user.id)
        
        # Prepare response
        return [
            PostResponse(
                id=post.id,
                text=post.text,
                user_id=post.user_id,
                user_email=user.email
            )
            for post in posts
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    token: str = Depends(get_token),
    db: Session = Depends(get_db)
):
    """
    Delete a post belonging to the authenticated user.
    
    Args:
        post_id: ID of the post to delete
        token: JWT token for authentication
        db: Database session dependency
    
    Returns:
        None: 204 No Content on success
    
    Raises:
        HTTPException: If authentication fails, post not found, or other errors
    """
    try:
        # Authenticate user
        user = get_current_user(token, db)
        
        # Delete post
        cache_service = CacheService()
        post_service = PostService(db, cache_service)
        post_service.delete_post(post_id, user.id)
        
        return None
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )