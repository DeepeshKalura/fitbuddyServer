from datetime import datetime
from typing import Optional
from typing import Literal
from pydantic import BaseModel, EmailStr, conint


class UserOut(BaseModel):
    id: int
    email: EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: str
    content: str
    published: bool


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


#! User schemas


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr
    password: str


class Users(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# ! auth schemas


# ! login


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


# ! For vote


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]  # Restricts dir to only be 0 or 1
