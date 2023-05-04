from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user

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


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
