from app import crud, models, schemas
from app.db import Session

# TODO error handling :)


def add_workout(db: Session, data: schemas.WorkoutCreate) -> models.Workout:
    db_workout = models.Workout()
    for exercise in data.exercises:
        db_exercise_set = models.ExerciseSet()
        db_exercise = crud.exercise.get(db, exercise.exercise_id)
        if db_exercise is None:
            ValueError("Mag niet")

        db_exercise_set.exercise_id = db_exercise.id

        for set in exercise.sets:
            db_set = models.Set(status=set.status, index=set.index)
            db.flush()

            for epv in set.values:
                db_epv = models.ExerciseParameterValue(value=epv.value)
                db_param = crud.exercise_parameter.get(db, epv.parameter_id)

                if db_param not in db_exercise.parameters:
                    ValueError("Mag niet")

                db_epv.exercise_id = db_exercise.id
                db_epv.parameter_id = db_param.id

                db_set.values.append(db_epv)

            db_exercise_set.sets.append(db_set)

        db_workout.exercises.append(db_exercise_set)
    return crud.workout.save(db, db_obj=db_workout)
