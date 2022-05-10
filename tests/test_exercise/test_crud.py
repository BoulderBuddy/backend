from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app.models import Exercise
from tests.conftest import TestData
from tests.test_exercise.util import exercise_crud_util


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
