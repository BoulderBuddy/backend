from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import schemas
from tests.conftest import TestData
from tests.test_exercise.util import exercise_crud_util


@pytest.mark.parametrize(
    "data",
    [
        schemas.ExerciseCreate(
            name="Oefening", parameters=[TestData.EXER_PARA_1, TestData.EXER_PARA_2]
        )
    ],
)
def test_create_exercise(db: Session, data: schemas.ExerciseCreate) -> None:
    obj = schemas.Exercise.from_orm(exercise_crud_util.insert_into_db(db, data))
    assert obj
    assert obj.name == data.name
    assert obj.parameters == data.parameters


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Henky",
            "parameters": [TestData.EXER_PARA_1],
        },
        {
            "name": "Henky",
        },
        {
            "parameters": [TestData.EXER_PARA_1],
        },
        {},
    ],
)
def test_update_exercise(db: Session, data: Dict[str, Any]) -> None:
    db_obj = exercise_crud_util.insert_into_db(db)
    obj = exercise_crud_util.update_into_db(db, db_obj, data)

    assert obj is not None
    assert obj.name == data.get("name") or db_obj.name
    assert obj.parameters == data.get("parameters") or db_obj.parameters
