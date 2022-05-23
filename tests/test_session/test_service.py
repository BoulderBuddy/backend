from app import schemas
from app.db import Session
from app.services.workout import add_workout
from tests.conftest import TestData

from .utils import create_workout


def test_crud(db: Session) -> None:
    workout_create = create_workout(
        TestData.EXERCISE_1, n_sets=2, value=15, status=schemas.SetStatus.COMPLETE
    )
    workout_create.exercises[0].sets[0].values[0].value = 33
    workout_create.exercises[0].sets[0].values[0].parameter_id = TestData.EXER_PARA_2.id
    workout_create.exercises[0].sets[0].status = schemas.SetStatus.PARTIAL

    db_workout = add_workout(db, workout_create)
    db_exercise_set = db_workout.exercises[0]
    first_set = db_exercise_set.sets[0]
    second_set = db_exercise_set.sets[1]

    assert db_workout
    assert db_exercise_set.exercise_id == TestData.EXERCISE_1.id

    assert len(db_exercise_set.sets) == 2
    assert first_set.status == schemas.SetStatus.PARTIAL
    assert second_set.status == schemas.SetStatus.COMPLETE

    assert first_set.values[0].value == 33
    assert second_set.values[0].value == 15
