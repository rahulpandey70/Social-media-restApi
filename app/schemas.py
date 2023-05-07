from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_At: datetime

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_At: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
