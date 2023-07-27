from fastapi import FastAPI, Body
from pydantic import BaseModel

# from fastapi.params import Body


app = FastAPI()

# request GET method and order matter in FastAPI


@app.get("/")
def root():
    return {"message": "Welcome to api"}


@app.get("/posts")
def get_posts():
    return {"data": "All posts"}


# title string and content string


class Post(BaseModel):
    title: str
    content: str


@app.post("/createposts")
async def create_post(new_post: Post):
    return {
        "data": f"tittle {new_post.title} and content {new_post.content} created successfully"
    }
