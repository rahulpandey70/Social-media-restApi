from fastapi import Body, FastAPI, Response, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"Data": posts}

# Create Post


@app.post("/posts", status_code=201)
async def createPost(post: Post):
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                (post.title, post.content, post.published))
    new_post = cur.fetchone()

    conn.commit()

    return {"message": new_post}

# Get Single Post


@app.get("/posts/{id}")
async def get_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} not found")
    return {"post detail": post}

# Delete Post


@app.delete("/posts/{id}", status_code=204)
async def delete_post(id: int):

    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deletedPost = cur.fetchone()
    conn.commit()

    if deletedPost == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    return Response(status_code=204)


# Update Post
@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                (post.title, post.content, post.published, str(id)))
    updatedPost = cur.fetchone()
    conn.commit()

    if updatedPost == None:
        raise HTTPException(
            status_code=404, detail=f"post with id {id} doesn't exist")

    return {"data": updatedPost}
