from fastapi import Body, FastAPI

app = FastAPI()

# request GET method and order matter in FastAPI


@app.get("/")
def root():
    return {"message": "Welcome to api"}


@app.get("/posts")
def get_posts():
    return {"data": "All posts"}


@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"data": "Create post"}
