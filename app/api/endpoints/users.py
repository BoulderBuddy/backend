from fastapi import APIRouter, Depends
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.api.responses import NotFoundResponse
from app.core.exceptions import NotFoundException
from app.schemas import User, UserCreate, UserUpdate

router = APIRouter()


def get_field_name(obj: object, field):
    gert = obj.__dict__
    return [x for (x, y) in gert.items() if y == field].pop()


def custom_validation_error(msg, obj, field_value, *, req_loc="body"):
    param_name = get_field_name(obj, field_value)
    return [ErrorWrapper(ValueError(msg), (req_loc, param_name))]


@router.get("/", response_model=list[User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.user.get_by_email(db, email=user.email):
        raise RequestValidationError(
            custom_validation_error("Email is already registered", user, user.email)
        )
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
    responses={**NotFoundResponse},
)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user_db = crud.user.get(db, user_id)
    if user_db is None:
        raise NotFoundException("User could not be found")

    if crud.user.get_by_email(db, email=user_update.email):
        raise RequestValidationError(
            custom_validation_error(
                "Email is already registered", user_update, user_update.email
            )
        )

    user = crud.user.update(db, db_obj=user_db, obj_in=user_update)
    return user
