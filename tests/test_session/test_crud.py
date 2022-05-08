from datetime import date
from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import TrainingSessionCreate, TrainingSessionUpdate
from tests.conftest import TestData


def insert_test_trainingsession_into_db(
    db: Session, data: Dict[str, Any] | None = None
) -> models.TrainingSession:
    if data is None:
        data = {
            "date": date.fromisocalendar(1990, 12, 5),
            "comment": "Hallo",
            "user_id": TestData.USER.id,
        }

    trainingsession_in = TrainingSessionCreate(**data)
    return crud.training_session.create(db, obj_in=trainingsession_in)


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
def test_create_trainingsession(db: Session, data: Dict[str, Any]) -> None:
    trainingsession = insert_test_trainingsession_into_db(db, data)

    assert trainingsession is not None
    assert trainingsession.comment == data.get("comment")
    assert trainingsession.date == data.get("date")
    assert trainingsession.user_id == data.get("user_id")


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
def test_update_trainingsession(db: Session, data: Dict[str, Any]) -> None:
    trainingsession_db = insert_test_trainingsession_into_db(db)

    trainingsession_update = TrainingSessionUpdate(**data)
    trainingsession = crud.training_session.update(
        db, db_obj=trainingsession_db, obj_in=trainingsession_update
    )

    assert trainingsession is not None
    assert (
        trainingsession.comment == trainingsession_update.comment
        or trainingsession_db.comment
    )
    assert (
        trainingsession.date == trainingsession_update.date or trainingsession_db.date
    )
    assert trainingsession.user_id == trainingsession_db.user_id
