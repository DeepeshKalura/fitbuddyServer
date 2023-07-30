from fastapi import FastAPI
from .database import engine
from app import model
from .router import post, user, auth
from .config import settings


# from fastapi.params import Body
model.Base.metadata.create_all(bind=engine)
app = FastAPI()

print(settings.DATABASE_NAME)
print("/n/n/n/n/n/n/n/n/n/n/n/n")
print(settings.DATABASE_USERNAME)
print(settings.DATABASE_PASSWORD)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to api"}
