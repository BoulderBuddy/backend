from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.deps import get_db
from app.api.responses import NotFoundResponse
from app.core.exceptions import NotFoundException
from app.db import KeyType

router = APIRouter()
# TODO tests for all


@router.get(
    "/{session_id}",
    response_model=schemas.TrainingSessionDetail,
    responses={**NotFoundResponse},
)
def read_single_training_session(session_id: KeyType, db: Session = Depends(get_db)):
    session = crud.session.get(db, session_id)
    if session is None:
        raise NotFoundException("Session could not be found")
    return session


@router.post("/", response_model=schemas.TrainingSessionDetail)
def create_training_session(
    data: schemas.TrainingSessionCreate, db: Session = Depends(get_db)
):
    return crud.session.create(db, obj_in=data)


@router.post(
    "/{session_id}/workouts",
    response_model=schemas.TrainingSessionDetail,
    responses={**NotFoundResponse},
)
def add_workout_to_session(
    session_id: KeyType, data: schemas.WorkoutCreate, db: Session = Depends(get_db)
):
    session = crud.session.get(db, session_id)
    if session is None:
        raise NotFoundException("Session could not be found")

    db_workout = add_workout(db, data)

    session.workouts.append(db_workout)
    return crud.session.save(db, db_obj=session)


# TODO move to service
def add_workout(db: Session, data: schemas.WorkoutCreate) -> models.Workout:
    db_workout = models.Workout()
    for exercise in data.exercises:
        db_exercise_set = models.ExerciseSet()
        db_exercise = crud.exercise.get(db, exercise.exercise_id)
        db_exercise_set.exercise = db_exercise

        for set in exercise.sets:
            db_set = models.Set(status=set.status, index=set.index)

            for epv in set.values:
                db_epv = models.ExerciseParameterValue(value=epv.value)
                db_param = crud.exercise_parameter.get(db, epv.parameter_id)

                if db_param not in db_exercise.parameters:
                    ValueError("Mag niet")

                db_epv.exercise = db_exercise
                db_epv.parameter = db_param

                db_set.values.append(db_epv)

            db_exercise_set.sets.append(db_set)

        db_workout.exercises.append(db_exercise_set)
    return crud.workout.save(db, db_obj=db_workout)
