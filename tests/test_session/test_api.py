from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.services.workout import upsert_workout
from tests.conftest import TestData

from .utils import create_session, create_workout

SESSION_ENDPOINT = "sessions"


def setup_database(db: Session):
    workout_data = create_workout(TestData.EXERCISE_1)
    session_create = create_session()

    db_obj = crud.session.create(db, obj_in=session_create)
    db_workout = upsert_workout(db, workout_data)
    db_obj.workouts.append(db_workout)
    return crud.session.save(db, db_obj=db_obj)


def test_read_training_session(client: TestClient, db: Session):
    db_obj = setup_database(db)

    r = client.get(f"{SESSION_ENDPOINT}/{db_obj.id}")

    assert r.status_code == 200
    assert r.json() is not None
