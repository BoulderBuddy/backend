from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import crud
from app.crud.crud_exercise import CRUDExercise, CRUDExerciseParameter
from app.models import Exercise, ExerciseParameter
from app.schemas import (
    ExerciseCreate,
    ExerciseParameterCreate,
    ExerciseParameterUpdate,
    ExerciseUpdate,
)
from tests.conftest import TestData
from tests.utils import CRUDTestUtil

_default_exer_para_data = ExerciseParameterCreate(name="mm", unit_type="int").__dict__
_default_exercise_data = ExerciseCreate(
    name="Piet", parameter_ids=[TestData.EXER_PARA_1.id, TestData.EXER_PARA_2.id]
).__dict__

exercise_parameter_crud_util = CRUDTestUtil[
    CRUDExerciseParameter,
    ExerciseParameter,
    ExerciseParameterCreate,
    ExerciseParameterUpdate,
](_default_exer_para_data, crud.exercise_parameter)

exercise_crud_util = CRUDTestUtil[
    CRUDExercise, Exercise, ExerciseCreate, ExerciseUpdate
](_default_exercise_data, crud.exercise)


@pytest.mark.parametrize("data", [{"name": "Fred", "unit_type": "int"}])
def test_create_exercise_parameter(db: Session, data: Dict[str, Any]) -> None:
    exercise_parameter_crud_util.create_assert(db, data)


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Oefening",
            "parameter_ids": [TestData.EXER_PARA_1.id, TestData.EXER_PARA_2.id],
        }
    ],
)
def test_create_exercise(db: Session, data: Dict[str, Any]) -> None:
    def mapper(db_obj: Exercise):
        db_obj_dict = db_obj.__dict__
        db_obj_dict["parameter_ids"] = [x.id for x in db_obj.parameters]
        return db_obj_dict

    exercise_crud_util.create_assert(db, data, db_obj_map=mapper)


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
    exercise_parameter_db = exercise_parameter_crud_util.insert_into_db(db)
    exercise_parameter = exercise_parameter_crud_util.update_into_db(
        db, exercise_parameter_db, data
    )

    assert exercise_parameter is not None
    assert exercise_parameter.name == data.get("name") or exercise_parameter_db.name
    assert (
        exercise_parameter.unit_type == data.get("unit_type")
        or exercise_parameter_db.unit_type
    )


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Henky",
            "parameter_ids": [TestData.EXER_PARA_1.id],
        },
        {
            "name": "Henky",
        },
        {
            "parameter_ids": [TestData.EXER_PARA_1.id],
        },
        {},
    ],
)
def test_update_exercise(db: Session, data: Dict[str, Any]) -> None:
    db_obj = exercise_crud_util.insert_into_db(db)
    obj = exercise_crud_util.update_into_db(db, db_obj, data)

    assert obj is not None
    assert obj.name == data.get("name") or db_obj.name
    assert [x.id for x in obj.parameters] == data.get("parameter_ids") or [
        x.id for x in db_obj.parameters
    ]
