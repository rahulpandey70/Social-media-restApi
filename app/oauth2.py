from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# SECRET_KEY
# ALGORITHM
# EXPIRE TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_TIME = settings.access_token_expire

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):

    copied_data = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME)
    copied_data.update({"exp": expire})

    jwt_token = jwt.encode(copied_data, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_access_token(token: str, credentials_exception):

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = decoded_token.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
