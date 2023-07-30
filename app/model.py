from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        nullable=False,
    )
    title = Column(
        String,
        nullable=False,
    )
    content = Column(
        String,
        nullable=False,
    )
    published = Column(
        Boolean,
        server_default="True",
        nullable=False,
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP,
        server_default="now()",
        nullable=False,
    )

    owner = relationship(
        "User",  # type: ignore
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False, unique=True)
    email = Column(
        String,
        nullable=False,
        unique=True,
    )
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP,
        server_default="now()",
        nullable=False,
    )


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
