""" Modules"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..password_handler import PasswordHandler

# API Router for Users API endpoints.
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
)
def create_user(user: schemas.UserCreate, db_user: Session = Depends(get_db)):
    """Create a new user"""
    hashed_password = PasswordHandler().hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db_user.add(new_user)
    db_user.commit()
    db_user.refresh(new_user)

    return new_user


@router.get(
    "/{user_id}",
    response_model=schemas.UserResponse,
)
def get_users_by_id(user_id: int, db_user: Session = Depends(get_db)):
    """ "Get users by user_id from database"""

    ret_user = (
        db_user.query(models.User).filter(models.User.id == user_id).first()
    )

    if ret_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with Id {user_id} was not found",
        )

    return ret_user
