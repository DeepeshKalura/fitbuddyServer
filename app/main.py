from fastapi import FastAPI

# from .database import engine
from .router import post, user, auth, votes
from .router import cors


# from fastapi.params import Body
# model.Base.metadata.create_all(bind=engine)
# ! This is not needed anymore, because we are using alembic for migrations
app = FastAPI()

cors.add_cors(app)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to api"}
