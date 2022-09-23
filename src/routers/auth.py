""" Modules"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, schemas
from ..password_handler import PasswordHandler

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    user_credentials: schemas.UserLogin,
    db_sess: Session = Depends(database.get_db),
):
    """User Login"""
    user = (
        db_sess.query(models.User)
        .filter(models.User.email == user_credentials.email)
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

    # create a token and return it
    return {"token": "sample token"}
