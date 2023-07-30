from fastapi import HTTPException, Response, status, Depends, APIRouter

from app import oauth2
from .. import model, schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/votes",
    tags=["Vote"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def createVote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {vote.post_id} not found",
        )
    vote_query = db.query(model.Vote).filter(
        model.Vote.post_id == vote.post_id, model.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Already upvoted"
            )
        new_vote = model.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"detail": "Upvoted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No vote found"
            )
        db.delete(found_vote)
        db.commit()
        return {"detail": "Downvoted"}
