from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import ExerciseCreate, ExerciseParameterCreate, ExerciseParameterUpdate
from tests.conftest import TestData
from tests.utils import insert_into_db_template

_default_exer_para_data = ExerciseParameterCreate(name="mm", unit_type="int").__dict__
_default_exercise_data = ExerciseCreate(
    name="Piet", parameter_ids=[TestData.EXER_PARA_1.id, TestData.EXER_PARA_2.id]
).__dict__

insert_exercise_parameter_into_db = insert_into_db_template(
    models.ExerciseParameter,
    ExerciseParameterCreate,
    crud.exercise_parameter,
    _default_exer_para_data,
)

insert_exercise_into_db = insert_into_db_template(
    models.Exercise,
    ExerciseCreate,
    crud.exercise,
    _default_exercise_data,
)


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Fred",
            "unit_type": "int",
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
            "unit_type": "int",
        },
        {
            "name": "Fred",
        },
        {
            "unit_type": "int",
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
