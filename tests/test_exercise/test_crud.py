from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import ExerciseParameterCreate, ExerciseParameterUpdate


def insert_exercise_parameter_into_db(
    db: Session, data: Dict[str, Any] | None = None
) -> models.ExerciseParameter:
    if data is None:
        data = {
            "name": "Fred",
            "unit_type": "Integer",
        }

    obj_in = ExerciseParameterCreate(**data)
    return crud.exercise_parameter.create(db, obj_in=obj_in)


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Fred",
            "unit_type": "Integer",
        },
    ],
)
def test_create_exercise_parameter(db: Session, data: Dict[str, Any]) -> None:
    exercise_parameter = insert_exercise_parameter_into_db(db, data)

    assert exercise_parameter is not None
    assert exercise_parameter.name == data.get("name")
    assert exercise_parameter.unit_type == data.get("unit_type")


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Fred",
            "unit_type": "Integer",
        },
        {
            "name": "Fred",
        },
        {
            "unit_type": "Integer",
        },
        {},
    ],
)
def test_update_exercise_parameter(db: Session, data: Dict[str, Any]) -> None:
    exercise_parameter_db = insert_exercise_parameter_into_db(db)

    exercise_parameter_update = ExerciseParameterUpdate(**data)
    exercise_parameter = crud.exercise_parameter.update(
        db, db_obj=exercise_parameter_db, obj_in=exercise_parameter_update
    )

    assert exercise_parameter is not None
    assert exercise_parameter.name == data.get("name") or exercise_parameter_db.name
    assert (
        exercise_parameter.unit_type == data.get("unit_type")
        or exercise_parameter_db.unit_type
    )
