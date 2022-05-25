from app import crud, models, schemas
from app.core.exceptions import NotFoundException
from app.db import Session

# TODO error handling :)
# TODO maybe not save in add_workout method


def add_exercise_set(
    db: Session, exercise: schemas.ExerciseSetUpsert, db_workout: models.Workout
):
    db_exercise_set = models.ExerciseSet()
    db_exercise = crud.exercise.get(db, exercise.exercise_id)
    if db_exercise is None:
        raise ValueError("Exercise does not exist")

    db_exercise_set.exercise_id = db_exercise.id

    for _set in exercise.sets:
        db_set = models.Set(status=_set.status, index=_set.index)

        for epv in _set.values:
            db_epv = models.ExerciseParameterValue(value=epv.value)
            db_param = crud.exercise_parameter.get(db, epv.parameter_id)

            db_epv.exercise_id = db_exercise.id
            db_epv.parameter_id = db_param.id
            db_epv.workout_id = db_workout.id

            db_set.values.append(db_epv)

        left = set(x.parameter_id for x in db_set.values)
        right = set(x.id for x in db_exercise.parameters)

        if missing_in_left := [x for x in right if x not in left]:
            raise ValueError(
                "Missing value(s) for exercise parameters: ", missing_in_left
            )

        if missing_in_right := [x for x in left if x not in right]:
            raise ValueError("Exercise does not have parameters: ", missing_in_right)

        db_exercise_set.sets.append(db_set)

    return db_exercise_set


def upsert_workout(db: Session, data: schemas.WorkoutUpsert) -> models.Workout:
    if not data.id:
        db_workout = crud.workout.save(db, db_obj=models.Workout())
    else:
        db_workout = crud.workout.get(db, data.id)
        if not db_workout:
            raise NotFoundException("Workout not found")

    db_workout.exercises = []

    for exercise in data.exercises:
        db_exercise_set = add_exercise_set(db, exercise, db_workout)
        db_workout.exercises.append(db_exercise_set)

    db_obj = crud.workout.save(db, db_obj=db_workout)
    return db_obj
