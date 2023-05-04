from fastapi import Body, FastAPI, Response, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# connect to database
while True:
    try:
        conn = psycopg2.connect(
            host='localhost', database='socialmediaapi', user='postgres', password='password123', cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Connnection to database is successfull")
        break
    except Exception as error:
        print("Connection to database is failed")
        print("Error: ", error)
        time.sleep(3)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Get Post
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts


# Create Post
@app.post("/posts", status_code=201, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get Single Post
@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} not found")

    return post


# Delete Post
@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):

    deletedPost = db.query(models.Post).filter(models.Post.id == id)

    if deletedPost.first() == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    deletedPost.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)


# Update Post
@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):

    updatedPost = db.query(models.Post).filter(models.Post.id == id)

    if updatedPost.first() == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    updatedPost.update(post.dict(), synchronize_session=False)

    db.commit()

    return updatedPost.first()


# Create User
@app.post("/users", status_code=201, response_model=schemas.UserResponse)
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
@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with id {id} doesn't exist")

    return user


# Get all user
@app.get("/users", status_code=200, response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users
