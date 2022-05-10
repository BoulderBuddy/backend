from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api.deps import get_db
from app.api.error_http import NotFoundResponse
from app.core.exceptions import NotFoundException
from app.schemas import ExerciseParameter, ExerciseParameterCreate
from app.schemas.exercise import ExerciseParameterUpdate

router = APIRouter()


@router.get("/", response_model=list[ExerciseParameter])
def read_all_parameters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.exercise_parameter.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=ExerciseParameter)
def create_exercise_parameter(
    parameter: ExerciseParameterCreate, db: Session = Depends(get_db)
):
    return crud.exercise_parameter.create(db, obj_in=parameter)


@router.put(
    "/{parameter_id}", response_model=ExerciseParameter, responses={**NotFoundResponse}
)
def update_exercise_parameter(
    parameter_id: int, parameter: ExerciseParameterUpdate, db: Session = Depends(get_db)
):
    parameter_db = crud.exercise_parameter.get(db, parameter_id)
    if parameter_db is None:
        raise NotFoundException("ExerciseParameter could not be found")
    return crud.exercise_parameter.update(db, db_obj=parameter_db, obj_in=parameter)
