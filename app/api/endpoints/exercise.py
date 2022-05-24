from fastapi import APIRouter, Depends, Response
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.api.error_http import custom_validation_error
from app.api.responses import NoContentResponse, NotFoundResponse
from app.core.exceptions import NotFoundException
from app.schemas import Exercise, ExerciseCreate, ExerciseUpdate

router = APIRouter()


@router.get("/", response_model=list[Exercise])
def read_all_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.exercise.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=Exercise)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    try:
        return crud.exercise.create(db, obj_in=exercise)
    except ValueError as e:
        raise RequestValidationError(
            custom_validation_error(e, exercise, exercise.parameters)
        )


@router.put("/{exercise_id}", response_model=Exercise, responses={**NotFoundResponse})
def update_exercise(
    exercise_id: int, exercise_update: ExerciseUpdate, db: Session = Depends(get_db)
):
    exercise_db = crud.exercise.get(db, exercise_id)
    if exercise_db is None:
        raise NotFoundException("Exercise could not be found")
    try:
        return crud.exercise.update(db, db_obj=exercise_db, obj_in=exercise_update)
    except ValueError as e:
        raise RequestValidationError(
            custom_validation_error(e, exercise_update, exercise_update.parameters)
        )


@router.delete("/{exercise_id}", responses={**NotFoundResponse, **NoContentResponse})
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise_db = crud.exercise.remove(db, id=exercise_id)
    if exercise_db is None:
        raise NotFoundException("Exercise could not be found")
    return Response(status_code=204)
