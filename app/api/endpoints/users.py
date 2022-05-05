from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.api.error_http import NotFoundResponse
from app.core.exceptions import NotFoundException
from app.schemas import user

router = APIRouter()


@router.get("/", response_model=list[user.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    return crud.user.create(db, obj_in=user)


@router.get("/{user_id}", response_model=user.User, responses={**NotFoundResponse})
def read_single_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.user.get(db, user_id)
    if user is None:
        raise NotFoundException("User could not be found")
    return user
