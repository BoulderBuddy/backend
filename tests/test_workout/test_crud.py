from datetime import date
from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import WorkoutCreate, WorkoutUpdate
from tests.conftest import TestData


def insert_test_workout_into_db(
    db: Session, data: Dict[str, Any] | None = None
) -> models.Workout:
    if data is None:
        data = {
            "date": date.fromisocalendar(1990, 12, 5),
            "comment": "Hallo",
            "user_id": TestData.USER.id,
        }

    workout_in = WorkoutCreate(**data)
    return crud.workout.create(db, obj_in=workout_in)


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
def test_create_workout(db: Session, data: Dict[str, Any]) -> None:
    workout = insert_test_workout_into_db(db, data)

    assert workout is not None
    assert workout.comment == data.get("comment")
    assert workout.date == data.get("date")
    assert workout.user_id == data.get("user_id")


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
def test_update_workout(db: Session, data: Dict[str, Any]) -> None:
    workout_db = insert_test_workout_into_db(db)

    workout_update = WorkoutUpdate(**data)
    workout = crud.workout.update(db, db_obj=workout_db, obj_in=workout_update)

    assert workout is not None
    assert workout.comment == workout_update.comment or workout_db.comment
    assert workout.date == workout_update.date or workout_db.date
    assert workout.user_id == workout_db.user_id
