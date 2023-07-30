from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .. import model, schemas, utils, oauth2
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Auth"],
)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    #! Error ye per thi
    user_credntials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        #! Error de rahi yai ye line --> this line does not have a silly typo error in above
        db.query(model.User)
        .filter(model.User.email == user_credntials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    if not utils.verify(user_credntials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

    # create a token
