""" Modules """
import logging
import os

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import post, user

app = FastAPI()

app.include_router(post.router)

app.include_router(user.router)

logging.basicConfig(filename="src/logs/database.log", level=logging.INFO)

models.Base.metadata.create_all(bind=engine)

load_dotenv()


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
