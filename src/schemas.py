from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Posts(BaseModel):
    title: str
    content: str
    published_on= str(datetime.now())
    rating: Optional[int]= None