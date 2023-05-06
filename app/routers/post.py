from fastapi import HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


# Get Post
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # posts = db.query(models.Post).filter(
    #     models.Post.owner_id == current_user.id).all()

    posts = db.query(models.Post).all()

    return posts


# Create Post
@router.post("/", status_code=201, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get Single Post
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} not found")

    return post


# Delete Post
@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    deletedPost = db.query(models.Post).filter(models.Post.id == id)

    post = deletedPost.first()

    if post == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Allowed!")

    deletedPost.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)


# Update Post
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    updatedPost = db.query(models.Post).filter(models.Post.id == id)

    post_query = updatedPost.first()

    if post_query == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    if post_query.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Allowed!")

    updatedPost.update(post.dict(), synchronize_session=False)

    db.commit()

    return updatedPost.first()
