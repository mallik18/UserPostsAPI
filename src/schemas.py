""" Modules"""
from pydantic import BaseModel

class Posts(BaseModel):
    """ Scheme for Posts"""
    title: str
    content: str
    published: bool = True
