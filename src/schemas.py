""" Modules"""
from datetime import datetime

from pydantic import BaseModel


class Posts(BaseModel):
    """Schema for Posts"""

    title: str
    content: str
    published: bool = True


class PostsResponse(BaseModel):
    """Schema for the response for a post"""

    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        """Pydantic's orm_mode will tell the Pydantic model to
        read the data even if it is not a dict, but an ORM model
        or any other arbitrary object with attributes
        """

        orm_mode = True
