from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# ALGORITHM
# EXPIRE TIME

SECRET_KEY = "NewVGZnyHjEh6u94dfLJZ8SqTs3qwJvpLyZVLYxR"
ALGORITHM = "HS256"
EXPIRE_TIME = 30


def create_access_token(data: dict):

    copied_data = data.copy()

    expire = datetime.now() + timedelta(minutes=EXPIRE_TIME)
    copied_data.update({"exp": expire})

    jwt_token = jwt.encode(copied_data, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token
