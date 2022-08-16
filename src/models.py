""" Modules"""
from sqlalchemy import Column, Integer, String, Boolean

from src.database import Base


class Post(Base):
    """ Scheme of Posts table in database"""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable= False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    #date_created = Column(TIMESTAMP, nullable=False)
