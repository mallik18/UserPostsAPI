""" Modules """
import logging
import os
from fastapi import FastAPI, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from src.schemas import Posts
from . import models
from .database import engine, get_db

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

logging.basicConfig(filename='src/logs/database.log',
                        level=logging.DEBUG)
while True:

    try:
        conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'),
                                user=os.getenv('USER'), password=os.getenv('PASSWORD'),
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull!")
        logging.info("Database connection was successfull!")
        break
    except psycopg2.Error as err:
        print("Connecting to database failed", err)
        logging.error(err)


@app.get("/")
async def root():
    """ Main entry point"""
    return {"message": "Hello World"}

@app.get("/sqlalchemy")
def test_sqlalchemy(db_posts: Session= Depends(get_db)):
    """ Test a database with a SQLAlchemy model """
    return {"message": "success"}

@app.get("/posts")
def get_posts():
    """ Get all posts from database"""
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Posts):
    """Create a new post and insert it into the database"""
    # returning * = Feature of Postgres database to return the query result

    cursor.execute(""" INSERT INTO posts(title, content, published)
                       VALUES (%s, %s, %s) RETURNING * """,
                        (new_post.title, new_post.content, new_post.published))
    ret_post = cursor.fetchone()
    conn.commit()
    return {"Inserted post detail": ret_post}


@app.get("/posts/{post_id}")
def get_posts_by_id(post_id: int):
    """"Get posts by post_id from database"""
    # above id is kept to int because if it is str then there may be SQL injections
    # afterwards we can convert it to str

    cursor.execute(""" SELECT * FROM posts WHERE id= %s """, (str(post_id), ))
    ret_post = cursor.fetchone()

    if ret_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id {post_id} was not found")

    return {"Requested post by id": ret_post}


@app.delete("/posts/{post_id}")
def delete_posts(post_id: int):
    """ Delete a post from the database"""
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """,
                       (str(post_id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id {post_id} does not exist!")

    return {"content":f"Post of id {post_id} deleted successfully"}

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Posts):
    """ Update a post """
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s
                       WHERE id = %s RETURNING * """,
                       (post.title, post.content, post.published, str(post_id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id {post_id} does not exist!")

    return {"UpdatedPost": updated_post}
