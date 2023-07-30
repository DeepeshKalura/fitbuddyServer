from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import model, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# ! I guess it should be implemented with graph ql or some other technique
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Users])
def getUsers(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Users)
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    return user


# ! graph ql

# ! Unknow Error --> two primary key resolve now
# ! Still in db showing two primary key which can be change currenltly


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Users)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Has the password hashed - user.password
    checking_user = db.query(model.User).filter(model.User.email == user.email).first()
    if checking_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists",
        )
    hash = utils.hash(user.password)
    user.password = hash
    new_user = model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


#! Either you need pre-define libary or improve some more in the code


#! I delete the user but gives me internal server error
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteUser(
    id: int,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user),
):
    user = db.query(model.User).filter(model.User.id == id)
    result = user.first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )
    if current_user.id != result.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with id {id} is not authorized to delete",
        )
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#! I amm guess there are better ways in which we can implemenent this
#! updating info I update it well this time
@router.patch("/", response_model=schemas.Users)
def updateUser(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_query = db.query(model.User).filter(model.User.email == user.email)
    result = user_query.first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user.email} not found",
        )

    updateData = {}
    if user.password:
        hash = utils.hash(user.password)
        updateData["password"] = hash

    if updateData:
        user_query.update(updateData)
        db.commit()

    return result
