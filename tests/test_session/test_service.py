from app import schemas
from app.db import Session
from app.services.workout import upsert_workout
from tests.conftest import TestData

from .utils import create_workout


def test_create_workout(db: Session) -> None:
    workout_create = create_workout(
        TestData.EXERCISE_1, n_sets=2, value=15, status=schemas.SetStatus.COMPLETE
    )
    workout_create.exercises[0].sets[0].values[0].value = 33
    workout_create.exercises[0].sets[0].status = schemas.SetStatus.PARTIAL

    db_workout = upsert_workout(db, workout_create)
    workout = schemas.Workout.from_orm(db_workout)
    exercise_set = workout.exercises[0]
    first_set = exercise_set.sets[0]
    second_set = exercise_set.sets[1]

    assert workout
    assert exercise_set.exercise.id == TestData.EXERCISE_1.id

    assert len(exercise_set.sets) == 2
    assert first_set.status == schemas.SetStatus.PARTIAL
    assert second_set.status == schemas.SetStatus.COMPLETE

    assert first_set.values[0].value == 33
    assert second_set.values[0].value == 15


def test_update_workout_different_exercise(db: Session) -> None:
    workout_create = create_workout(TestData.EXERCISE_1)
    db_workout_create = upsert_workout(db, workout_create)

    workout_update = create_workout(TestData.EXERCISE_2)
    workout_update.id = db_workout_create.id
    db_workout = upsert_workout(db, workout_update)

    workout = schemas.Workout.from_orm(db_workout)
    exercise_set = workout.exercises[0]

    assert workout
    assert exercise_set.exercise.id == TestData.EXERCISE_2.id
