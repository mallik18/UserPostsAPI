""" Modules to use SQLALCHEMY ORM to interact with Database"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_USER=os.getenv('POSTGRES_USER')
PASSWORD=os.getenv('PASSWORD')
HOST=os.getenv('HOST')
DBNAME=os.getenv('DBNAME')


#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/
#                           hostname>/<database_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{PASSWORD}@{HOST}/{DBNAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """ Session/Connection to Database """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
