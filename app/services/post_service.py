from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.post_model import Post
from app.models.user_model import User
from app.schemas.post_schema import PostCreate, PostResponse
from app.database import get_db
from app.services.cache_service import CacheService
from app.exceptions import NotFoundException

class PostService:
    """
    Service layer for post-related operations.
    """
    
    def __init__(self, db: Session, cache_service: CacheService):
        self.db = db
        self.cache_service = cache_service
    
    def create_post(self, post_data: PostCreate, user_id: int) -> Post:
        """
        Create a new post for a user.
        
        Args:
            post_data: Post creation data
            user_id: ID of the user creating the post
        
        Returns:
            Post: The created post
        """
        db_post = Post(text=post_data.text, user_id=user_id)
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        
        # Invalidate cache for this user's posts
        self.cache_service.invalidate_user_posts(user_id)
        
        return db_post
    
    def get_user_posts(self, user_id: int) -> List[Post]:
        """
        Get all posts for a user, using cache when possible.
        
        Args:
            user_id: ID of the user to get posts for
        
        Returns:
            List[Post]: List of the user's posts
        """
        # Try to get from cache first
        cached_posts = self.cache_service.get_user_posts(user_id)
        if cached_posts is not None:
            return cached_posts
        
        # If not in cache, fetch from DB
        posts = self.db.query(Post).filter(Post.user_id == user_id).all()
        
        # Store in cache
        self.cache_service.set_user_posts(user_id, posts)
        
        return posts
    
    def delete_post(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post if it belongs to the user.
        
        Args:
            post_id: ID of the post to delete
            user_id: ID of the user attempting deletion
        
        Returns:
            bool: True if deletion was successful
        
        Raises:
            NotFoundException: If post doesn't exist or doesn't belong to user
        """
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise NotFoundException("Post not found")
        if post.user_id != user_id:
            raise NotFoundException("Post does not belong to user")
        
        self.db.delete(post)
        self.db.commit()
        
        # Invalidate cache for this user's posts
        self.cache_service.invalidate_user_posts(user_id)
        
        return True