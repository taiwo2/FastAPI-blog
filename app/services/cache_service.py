from datetime import timedelta
from typing import List, Optional
from app.models.post_model import Post
from app.config import settings
import redis

class CacheService:
    """
    Service for handling in-memory caching using Redis.
    """
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host="localhost",
            port=6379,
            db=0,
            decode_responses=True
        )
    
    def _get_user_posts_key(self, user_id: int) -> str:
        """
        Generate cache key for user posts.
        
        Args:
            user_id: ID of the user
        
        Returns:
            str: Cache key
        """
        return f"user:{user_id}:posts"
    
    def get_user_posts(self, user_id: int) -> Optional[List[Post]]:
        """
        Get cached posts for a user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            Optional[List[Post]]: Cached posts or None if not in cache
        """
        # In a real implementation, we would serialize/deserialize Post objects
        # For simplicity, we'll just return None here
        return None
    
    def set_user_posts(self, user_id: int, posts: List[Post]) -> None:
        """
        Cache posts for a user.
        
        Args:
            user_id: ID of the user
            posts: List of posts to cache
        """
        # In a real implementation, we would serialize Post objects
        # For now, we'll just set a flag that posts are cached
        key = self._get_user_posts_key(user_id)
        self.redis_client.setex(key, settings.CACHE_EXPIRE_SECONDS, "1")
    
    def invalidate_user_posts(self, user_id: int) -> None:
        """
        Invalidate cached posts for a user.
        
        Args:
            user_id: ID of the user
        """
        key = self._get_user_posts_key(user_id)
        self.redis_client.delete(key)