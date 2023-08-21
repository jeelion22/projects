from typing import Union, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel  # decribes the schema, validates user post
from random import randrange
import psycopg2
import os
from psycopg2.extras import RealDictCursor  # for getting column names of the db table
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

db_user_name = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PWD")


app = FastAPI()


class Post(BaseModel):  # automatically performs validation
    title: str
    content: str
    published: bool = True  # property that set as optional
    # rating: Optional[int] = None  # gets fully optional pproperty


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user=db_user_name,
            password=db_password,
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connecting to the database")
        print("Error: ", error)
        time.sleep(2)  # sleeps for 2 seconds for reconnectiong dB

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like to pizza", "id": 2},
]


# finds the specific post based on the id provided
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for ind, post in enumerate(my_posts):
        if post["id"] == id:
            return ind


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"message": "success"}


# path operation
@app.get(
    "/"
)  # @ is for decorator representation, app is the name of the app, and get is the http method "/" represents the root path
def read_root():  # the func name does not matter; but stick with descriptive
    return {"message": "Welcome to my API"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}


# requests GET method with url "/posts"
@app.get("/posts")
def get_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id""")
    my_posts = (
        cursor.fetchall()
    )  # this function fetches all the entries from the table of the database

    return {"data": my_posts}


# post method
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published),
    )
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[-1]

    return {"details": latest_post}


@app.get("/posts/{id}")  # {id} field represents path parameter
def get_post(
    id: int,  # response: Response
):  # when define the argument type it automatically converts to the specified type
    # no more required response instance from Response
    # fetch a post from db
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # # instead of giving null, wants to print error if the post
        # # is not available
        # return {"message": f"post with id: {id} was not found"}
        # instead of doing all of the above we can use http exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post detail": post}


# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # when we delete someting we can use status code
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)

    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    # my_posts.pop(index)

    # return {"message": "post was succesfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update path operation
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    # index = find_index_post(id)

    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    # post_dict = post.dict()
    # post_dict["id"] = id
    # my_posts[index] = post_dict
    return {"data": updated_post}
