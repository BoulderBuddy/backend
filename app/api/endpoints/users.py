from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.api.error_http import AlreadyExistsResponse, NotFoundResponse
from app.core.exceptions import AlreadyExistsException, NotFoundException
from app.schemas import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=list[User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=User, responses={**AlreadyExistsResponse})
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.user.get_by_email(db, email=user.email):
        raise AlreadyExistsException("Email is already registered", user.email)
    return crud.user.create(db, obj_in=user)


@router.get("/{user_id}", response_model=User, responses={**NotFoundResponse})
def read_single_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.user.get(db, user_id)
    if user is None:
        raise NotFoundException("User could not be found")
    return user


@router.put(
    "/{user_id}",
    response_model=User,
    responses={**NotFoundResponse, **AlreadyExistsResponse},
)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user_db = crud.user.get(db, user_id)
    if user_db is None:
        raise NotFoundException("User could not be found")

    if crud.user.get_by_email(db, email=user_update.email):
        raise AlreadyExistsException("Email is already registered", user_update.email)

    user = crud.user.update(db, db_obj=user_db, obj_in=user_update)
    return user
