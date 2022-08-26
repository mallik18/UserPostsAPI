""" Modules """
import logging
import os
from typing import List

import psycopg2
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

load_dotenv()

# this below line
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(filename="src/logs/database.log", level=logging.INFO)
while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("HOST"),
            dbname=os.getenv("DBNAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("PASSWORD"),
            cursor_factory=RealDictCursor,
        )

        cursor = conn.cursor()
        print("Database connection was successfull!")
        logging.info("Database connection was successfull!")
        break
    except psycopg2.Error as err:
        print("Connecting to database failed", err)
        logging.error(err)


@app.get("/")
async def root():
    """Main entry point"""
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.PostsResponse])
def get_posts(db_posts: Session = Depends(get_db)):
    """Get all posts from database"""

    posts = db_posts.query(models.Post).all()
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Posts were not found",
        )

    return posts


@app.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostsResponse,
)
def create_posts(new_post: schemas.Posts, db_posts: Session = Depends(get_db)):
    """Create a new post and insert it into the database"""

    ret_post = models.Post(**new_post.dict())
    db_posts.add(ret_post)
    db_posts.commit()
    db_posts.refresh(ret_post)

    return ret_post


@app.get("/posts/{post_id}", response_model=schemas.PostsResponse)
def get_posts_by_id(post_id: int, db_posts: Session = Depends(get_db)):
    """ "Get posts by post_id from database"""

    ret_post = (
        db_posts.query(models.Post).filter(models.Post.id == post_id).first()
    )

    if ret_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id {post_id} was not found",
        )

    return ret_post


@app.delete("/posts/{post_id}")
def delete_posts(post_id: int, db_posts: Session = Depends(get_db)):
    """Delete a post from the database"""

    ret_post = db_posts.query(models.Post).filter(models.Post.id == post_id)

    if ret_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id {post_id} does not exist!",
        )

    ret_post.delete(synchronize_session=False)
    db_posts.commit()

    return {"content": f"Post of id {post_id} deleted successfully"}


@app.put("/posts/{post_id}", response_model=schemas.PostsResponse)
def update_post(
    post_id: int,
    updated_post: schemas.Posts,
    db_posts: Session = Depends(get_db),
):
    """Update a post"""

    post_query = db_posts.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with Id {post_id} does not exist!",
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db_posts.commit()

    return post_query.first()
