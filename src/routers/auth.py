""" Modules"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, schemas
from ..oauth2 import GenerateJWTToken
from ..password_handler import PasswordHandler

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.JWTToken)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db_sess: Session = Depends(database.get_db),
):
    """User Login Authentication and return JWT token"""
    # user_credentials dict contains username and password
    # instead of email and password because of OAuth2PasswordRequestForm
    user = (
        db_sess.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
        )

    if not PasswordHandler().verify_password(
        user_credentials.password, user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
        )
    access_token = GenerateJWTToken().create_access_token(
        data={"user_id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
