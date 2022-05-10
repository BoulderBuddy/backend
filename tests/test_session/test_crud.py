from datetime import date
from typing import Any, Dict

import pytest
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import TrainingSessionCreate
from tests.conftest import TestData
from tests.utils import CRUDTestUtil

_default_training_session_data = TrainingSessionCreate(
    date=date.fromisocalendar(1990, 12, 5), comment="Hallo", user_id=TestData.USER.id
).__dict__


training_session_crud_util = CRUDTestUtil[
    crud.CRUDTrainingSession, models.TrainingSession
](_default_training_session_data, crud.training_session)


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
    training_session_crud_util.create_assert(db, data)


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
        {},
    ],
)
def test_update_training_session(db: Session, data: Dict[str, Any]) -> None:
    training_session_db = training_session_crud_util.insert_into_db(db)
    training_session = training_session_crud_util.update_into_db(
        db, training_session_db, data
    )

    assert training_session is not None
    assert (
        training_session.comment == data.get("comment") or training_session_db.comment
    )
    assert training_session.date == data.get("date") or training_session_db.date
    assert training_session.user_id == training_session_db.user_id
