from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randint


# from fastapi.params import Body


app = FastAPI()

# request GET method and order matter in FastAPI


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title1", "content": "content1", "published": True, "rating": 5, "id": 1},
    {"title": "title2", "content": "content2", "published": True, "rating": 4, "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

    return None


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

    return 0


@app.get("/")
def root():
    return {"message": "Welcome to api"}


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if post == None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id {id} not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return {"data": post}


# title string and content string


@app.post("/createposts")
async def create_post(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict["id"] = randint(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    post = find_post(id)
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    post_index = find_post_index(id)
    if post_index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[post_index] = post_dict
    return {"data": post_dict}
