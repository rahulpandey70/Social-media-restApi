from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/users"
)


# Create user
@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # Hash the password
    hashed_password = utils.hashPassword(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    # Check email is already exist
    if new_user.email == user.email:
        raise HTTPException(status_code=409, detail=f"Email already exist.")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get single user
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} doesn't exist")

    return user


# Get all user
@router.get("/", status_code=200, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users
