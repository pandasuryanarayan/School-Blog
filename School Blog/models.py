from pydantic import BaseModel
from typing import Optional

class BlogPost(BaseModel):
    id: str                # Custom ID from the frontend
    title: str
    content: str
    author: str
    createdAt: Optional[str] = None  # Automatically set on the backend

    class Config:
        orm_mode = True

class BlogPostInDB(BlogPost):
    pass  # No additional fields are necessary