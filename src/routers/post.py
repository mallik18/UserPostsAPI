""" Modules"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

# API Router for Posts API endpoints.
router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostsResponse])
def get_posts(db_posts: Session = Depends(get_db)):
    """Get all posts from database"""

    posts = db_posts.query(models.Post).all()
    if posts is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Posts were not found",
        )

    return posts


@router.post(
    "/",
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


@router.get("/totalpostscount")
def get_total_posts_count(db_posts: Session = Depends(get_db)):
    """ "Get total posts count from database"""

    ret_post = db_posts.query(models.Post).count()

    if ret_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Total number of posts are zero",
        )

    return ret_post


@router.get("/{post_id}", response_model=schemas.PostsResponse)
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


@router.delete("/{post_id}")
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


@router.put("/{post_id}", response_model=schemas.PostsResponse)
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
