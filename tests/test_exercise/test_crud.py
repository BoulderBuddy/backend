from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import schemas
from app.api.endpoints.exercise import create_exercise
from tests.conftest import TestData
from tests.test_exercise.util import exercise_crud_util


@pytest.mark.parametrize(
    "data",
    [
        schemas.ExerciseCreate(
            name="Oefening",
            parameters=[TestData.EXER_PARA_1, TestData.EXER_PARA_2],
        )
    ],
)
def test_create_exercise(db: Session, data: schemas.ExerciseCreate) -> None:
    obj = schemas.Exercise.from_orm(create_exercise(data, db=db))
    assert obj
    assert obj.name == data.name
    assert [x.id for x in obj.parameters] == [x.id for x in data.parameters]


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

    if name := data.get("name"):
        assert obj.name == name
    else:
        assert obj.name == db_obj.name

    if params := data.get("parameters"):
        assert [x.id for x in obj.parameters] == [x.id for x in params]
    else:
        assert obj.parameters == db_obj.parameters
