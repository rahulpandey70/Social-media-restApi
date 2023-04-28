from fastapi import Body, FastAPI, Response, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title1", "content": "content for title1", "id": 1},
    {"title": "title2", "content": "content for title2", "id": 2},
    {"title": "title3", "content": "content for title3", "id": 3}
]

# Find Post Through Id


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# Find index
def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Get Post


@app.get("/posts")
async def getPost():
    return {"Data": my_posts}

# Create Post


@app.post("/posts", status_code=201)
async def createPost(newPost: Post):
    posts = newPost.dict()
    posts["id"] = randrange(0, 1000000)
    my_posts.append(posts)
    return {"message": newPost}

# Get Single Post


@app.get("/posts/{id}")
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} not found")
    print(post)
    return {"post detail": post}

# Delete Post


@app.delete("/posts/{id}", status_code=204)
async def delete_post(id: int):

    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    my_posts.pop(index)
    return Response(status_code=204)


# Update Post
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):

    index = find_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    post = post.dict()
    post["id"] = id
    my_posts[index] = post

    return {"data": post}
