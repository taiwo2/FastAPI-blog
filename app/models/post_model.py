from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base):
    """
    SQLAlchemy model representing a blog post.
    
    Attributes:
        id (int): Primary key
        text (str): Content of the post
        user_id (int): Foreign key to the user who created the post
        user (relationship): Relationship to the User model
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    user = relationship("User", back_populates="posts")