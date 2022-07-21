from fastapi import FastAPI, status, HTTPException, Response
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

from src.schemas import Posts


app = FastAPI()

logging.basicConfig(filename ='src/logs/database.log',
                        level = logging.DEBUG)
while True:
    
    try:
        conn = psycopg2.connect(host= 'localhost', dbname= 'UserPostsAPI', user= 'postgres',
                                password= 'changed#', cursor_factory= RealDictCursor) 
        cursor = conn.cursor()
        print("Database connection was successfull!")
        logging.info("Database connection was successfull!")
        break
    except BaseException as err:
        print("Connecting to database failed", err)
        logging.error(err)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code= status.HTTP_201_CREATED)
async def create_posts(new_post: Posts):
    cursor.execute(""" INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING * """,\
                        (new_post.title, new_post.content, new_post.published))
    ret_post = cursor.fetchone()
    conn.commit()
    return {"Inserted post detail": ret_post}

@app.get("/posts/{id}")
async def get_posts_by_id(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id= %s """, (str(id), ))
    ret_post = cursor.fetchone()

    if ret_post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id {id} was not found")

    return {"Requested post by id": ret_post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_posts(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"Post with Id {id} does not exist!")

    return Response(status_code= status.HTTP_204_NO_CONTENT)
