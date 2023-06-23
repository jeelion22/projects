from typing import Union, Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel  # decribes the schema, validates user post
from random import randrange

app = FastAPI()


class Post(BaseModel):  # automatically performs validation
    title: str
    content: str
    published: bool = True  # property that set as optional
    rating: Optional[int] = None  # gets fully optional pproperty


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


# path operation
@app.get(
    "/"
)  # @ is for decorator representation, app is the name of the app, and get is the http method "/" represents the root path
def read_root():  # the func name does not matter; but stick with descriptive
    return {"message": "Welcome to my API"}


# requests GET method with url "/posts"
@app.get("/posts")
def get_post():
    return {"data": my_posts}


# post method


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[-1]

    return {"details": latest_post}


@app.get("/posts/{id}")  # {id} field represents path parameter
def get_post(
    id: int,  # response: Response
):  # when define the argument type it automatically converts to the specified type
    # no more required response instance from Response
    post = find_post(id)
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
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )

    my_posts.pop(index)

    return {"message": "post was succesfully deleted"}


# update path operation
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
