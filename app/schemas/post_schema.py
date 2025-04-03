from pydantic import BaseModel, Field
from typing import Optional

class PostBase(BaseModel):
    """
    Base schema for post data.
    """
    text: str = Field(..., min_length=1, max_length=10000, 
                     example="This is a sample blog post.")

class PostCreate(PostBase):
    """
    Schema for post creation.
    """
    pass

class PostInDB(PostBase):
    """
    Schema for post data stored in database.
    """
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

class PostResponse(PostInDB):
    """
    Schema for post response (includes user email).
    """
    user_email: str