from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas

router = APIRouter(
    prefix="/posts"
)


# Get Post
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()

    return posts


# Create Post
@router.post("/", status_code=201, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get Single Post
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} not found")

    return post


# Delete Post
@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):

    deletedPost = db.query(models.Post).filter(models.Post.id == id)

    if deletedPost.first() == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    deletedPost.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)


# Update Post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):

    updatedPost = db.query(models.Post).filter(models.Post.id == id)

    if updatedPost.first() == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    updatedPost.update(post.dict(), synchronize_session=False)

    db.commit()

    return updatedPost.first()
