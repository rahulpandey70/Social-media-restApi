from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, utils, oauth2


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
def login(user_info: schemas.UserLogin, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_info.email).first()

    if not user:
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")

    if not utils.verifyPassword(user_info.password, user.password):
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")

    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}
