from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from .util import exercise_parameter_crud_util


@pytest.mark.parametrize("data", [{"name": "Fred", "unit_type": "int"}])
def test_create_exercise_parameter(db: Session, data: Dict[str, Any]) -> None:
    exercise_parameter_crud_util.create_assert(db, data)


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
