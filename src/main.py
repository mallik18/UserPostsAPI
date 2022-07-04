from fastapi import FastAPI

from src.schemas import Posts

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"data": "This is your post"}

@app.post("/posts")
async def create_posts(new_post: Posts):
    print(new_post)
    return {"new_post": new_post.dict()}
