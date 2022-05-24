from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.api.responses import NotFoundResponse
from app.core.exceptions import NotFoundException
from app.db import KeyType
from app.services.workout import add_workout

router = APIRouter()
# TODO tests for all


@router.get("/", response_model=list[schemas.TrainingSession])
def read_all_training_sessions(db: Session = Depends(get_db)):
    return crud.session.get_multi(db)


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
