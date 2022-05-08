from datetime import date
from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import TrainingSessionCreate, TrainingSessionUpdate
from tests.conftest import TestData


def insert_test_training_session_into_db(
    db: Session, data: Dict[str, Any] | None = None
) -> models.TrainingSession:
    if data is None:
        data = {
            "date": date.fromisocalendar(1990, 12, 5),
            "comment": "Hallo",
            "user_id": TestData.USER.id,
        }

    training_session_in = TrainingSessionCreate(**data)
    return crud.training_session.create(db, obj_in=training_session_in)


@pytest.mark.parametrize(
    "data",
    [
        {
            "date": date.fromisocalendar(1990, 12, 5),
            "comment": "Hallo",
            "user_id": TestData.USER.id,
        },
        {
            "date": date.fromisocalendar(1990, 12, 5),
            "user_id": TestData.USER.id,
        },
    ],
)
def test_create_training_session(db: Session, data: Dict[str, Any]) -> None:
    training_session = insert_test_training_session_into_db(db, data)

    assert training_session is not None
    assert training_session.comment == data.get("comment")
    assert training_session.date == data.get("date")
    assert training_session.user_id == data.get("user_id")


@pytest.mark.parametrize(
    "data",
    [
        {
            "date": date.fromisocalendar(2001, 3, 1),
            "comment": "Frikandel",
        },
        {
            "comment": "Frikandel",
        },
        {
            "date": date.fromisocalendar(2001, 3, 1),
        },
    ],
)
def test_update_training_session(db: Session, data: Dict[str, Any]) -> None:
    training_session_db = insert_test_training_session_into_db(db)

    training_session_update = TrainingSessionUpdate(**data)
    training_session = crud.training_session.update(
        db, db_obj=training_session_db, obj_in=training_session_update
    )

    assert training_session is not None
    assert (
        training_session.comment == training_session_update.comment
        or training_session_db.comment
    )
    assert (
        training_session.date == training_session_update.date
        or training_session_db.date
    )
    assert training_session.user_id == training_session_db.user_id
