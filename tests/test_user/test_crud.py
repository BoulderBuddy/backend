from sqlalchemy.orm import Session

from app import crud
from app.schemas.user import UserCreate


def test_create_user(db: Session) -> None:
    email = "Henk@tank.com"
    user_in = UserCreate(email=email)
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email
