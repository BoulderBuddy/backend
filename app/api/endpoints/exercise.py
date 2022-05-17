from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.api.responses import NoContentResponse, NotFoundResponse
from app.core.exceptions import NotFoundException
from app.schemas import Exercise, ExerciseCreate, ExerciseUpdate

router = APIRouter()


@router.get("/", response_model=list[Exercise])
def read_all_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.exercise.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=Exercise)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    return crud.exercise.create(db, obj_in=exercise)


@router.put("/{exercise_id}", response_model=Exercise, responses={**NotFoundResponse})
def update_exercise(
    exercise_id: int, exercise_update: ExerciseUpdate, db: Session = Depends(get_db)
):
    exercise_db = crud.exercise.get(db, exercise_id)
    if exercise_db is None:
        raise NotFoundException("Exercise could not be found")

    exercise = crud.exercise.update(db, db_obj=exercise_db, obj_in=exercise_update)
    return exercise


@router.delete("/{exercise_id}", responses={**NotFoundResponse, **NoContentResponse})
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise_db = crud.exercise.remove(db, id=exercise_id)
    if exercise_db is None:
        raise NotFoundException("Exercise could not be found")
    return Response(status_code=204)
