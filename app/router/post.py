from fastapi import HTTPException, Response, status, Depends, APIRouter

from app import oauth2
from .. import model, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    tags=["Posts"],
)


@router.get("/posts", status_code=status.HTTP_200_OK, response_model=list[schemas.Post])
def getPosts(
    db: Session = Depends(get_db),
    limit: int = 20,
    skip: int = 0,
    search: Optional[str] = "",
):
    post = (
        db.query(model.Post)
        .filter(model.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return post


@router.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def getPost(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    #! error here --> current_user: int = Depends(oauth2.get_current_user), because can't be int
    current_user: model.User = Depends(oauth2.get_current_user),
):
    new_post = model.Post(
        #! title=post.title, content=post.content, published=post.published
        #! unsufficent way
        owner_id=current_user.id,
        **post.model_dump(),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(
    id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    post = db.query(model.Post).filter(model.Post.id == id)
    result = post.first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    if result.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post with id {id} not owned by you",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def updatePost(
    id: int,
    post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    result = post_query.first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )
    if result.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post with id {id} not owned by you",
        )
    table = model.Post.__table__
    values = {table.columns[name]: value for name, value in post.model_dump().items()}
    post_query.update(values)
    db.commit()
    return post_query.first()
