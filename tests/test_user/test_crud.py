import pytest
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserUpdate

from .util import user_crud_util


@pytest.mark.parametrize(
    "data",
    [
        UserCreate(
            first_name="Bert",
            surname="van Ernie",
            email="bert@ernie.com",
            is_superuser=True,
        ),
        UserCreate(first_name="Bert", email="bert@ernie.com", is_superuser=True),
        UserCreate(first_name="Bert", surname="van Ernie", email="bert@ernie.com"),
        UserCreate(email="bert@ernie.com", is_superuser=True),
        UserCreate(email="bert@ernie.com"),
    ],
)
def test_create_user(db: Session, data: UserCreate) -> None:
    user_crud_util.create_assert(db, data)


@pytest.mark.parametrize(
    "data",
    [
        UserUpdate(
            first_name="Bert",
            surname="van Ernie",
            email="bert@ernie.com",
            is_superuser=True,
        ),
        UserUpdate(first_name="Bert", email="bert@ernie.com", is_superuser=True),
        UserUpdate(first_name="Bert", surname="van Ernie"),
        UserUpdate(email="bert@ernie.com", is_superuser=True),
        UserUpdate(email="bert@ernie.com"),
        UserUpdate(),
    ],
)
@pytest.mark.parametrize("fields", [["email", "first_name", "surname", "is_superuser"]])
def test_update_user(db: Session, data: UserUpdate, fields: list[str]) -> None:
    db_obj = user_crud_util.insert_into_db(db)
    obj = user_crud_util.update_into_db(db, db_obj, data)

    assert obj is not None
    for field in fields:
        assert getattr(obj, field) == getattr(data, field) or getattr(db_obj, field)
