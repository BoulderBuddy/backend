from datetime import date

from app import models, schemas
from app.db import KeyType


def create_epvs(
    exercise: models.Exercise, *, value: int = 10
) -> list[schemas.ExerciseParameterValueUpsert]:
    return [
        schemas.ExerciseParameterValueUpsert(parameter_id=param.id, value=value)
        for param in exercise.parameters
    ]


def create_exercise_set(
    exercise: models.Exercise,
    *,
    n_sets: int = 1,
    value: int = 10,
    status: schemas.SetStatus = schemas.SetStatus.COMPLETE,
) -> list[schemas.SetUpsert]:
    set_creates = [
        schemas.SetUpsert(
            index=i,
            status=status,
            values=create_epvs(exercise, value=value),
        )
        for i in range(n_sets)
    ]

    bla = schemas.ExerciseSetUpsert(exercise_id=exercise.id, sets=set_creates)

    return bla


def create_workout(exercise: models.Exercise, **kw):
    exercise = create_exercise_set(exercise, **kw)
    return schemas.WorkoutUpsert(exercises=[exercise])


def create_session(
    *,
    date=date.fromisocalendar(1995, 34, 5),
    comment="mooi man",
    user_id: KeyType = None,
):
    return schemas.TrainingSessionCreate(date=date, comment=comment, user_id=user_id)
