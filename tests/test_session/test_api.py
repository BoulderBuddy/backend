from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.endpoints.session import add_workout
from tests.conftest import TestData

# TODO move to utils


def create_epvs(
    exercise: models.Exercise, *, value: int = 10
) -> list[schemas.ExerciseParameterValueCreate]:
    return [
        schemas.ExerciseParameterValueCreate(parameter_id=param.id, value=value)
        for param in exercise.parameters
    ]


def create_exercise_set(
    exercise: models.Exercise,
    *,
    n_sets: int = 1,
    value: int = 10,
    status: schemas.SetStatus = schemas.SetStatus.COMPLETE,
) -> list[schemas.SetCreate]:
    set_creates = [
        schemas.SetCreate(
            index=i,
            status=status,
            values=create_epvs(exercise, value=value),
        )
        for i in range(n_sets)
    ]

    bla = schemas.ExerciseSetCreate(exercise_id=exercise.id, sets=set_creates)

    return bla


def test_crud(db: Session) -> None:
    exercise = create_exercise_set(TestData.EXERCISE_1, n_sets=3)
    data = schemas.WorkoutCreate(exercises=[exercise])
    db_workout = add_workout(db, data)
    assert db_workout


SESSION_ENDPOINT = "sessions"


def test_read_training_session(client: TestClient, db: Session):
    # TODO refactor away
    # Setup data
    exercise = create_exercise_set(TestData.EXERCISE_1, n_sets=3)
    data = schemas.WorkoutCreate(exercises=[exercise])
    db_workout = add_workout(db, data)
    db_obj = models.TrainingSession()
    db_obj.date = date.fromisocalendar(1995, 34, 5)
    db_obj.comment = "mooi man"
    db_obj.workouts.append(db_workout)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    r = client.get(f"{SESSION_ENDPOINT}/{db_obj.id}")

    assert r.status_code == 200
    assert r.json() is not None
