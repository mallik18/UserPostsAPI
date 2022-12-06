""" Modules """


import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

# SECRET_KEY
# ALGORITHM
# EXPIRATION_TIME
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class GenerateJWTToken:
    """Generate JWT Tokens"""

    def __init__(self):
        """init method"""

    def create_access_token(self, data: dict):
        """Creating a new access token"""
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode["exp"] = expire

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_access_token(self, token: str, credentials_exception):
        """Verify access token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("users_id")

            if user_id is None:
                raise credentials_exception
            token_data = schemas.JWTTokenData(id=id)

        except JWTError as err:
            raise credentials_exception from err

        return token_data

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        """Get current user"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        return self.verify_access_token(token, credentials_exception)
