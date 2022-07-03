from lib2to3.pytree import Base
from pydantic import BaseModel

class Posts(BaseModel):
    title: str
    content: str