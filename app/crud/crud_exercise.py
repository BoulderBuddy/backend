from app.crud.base import CRUDBase
from app.models import Exercise, ExerciseParameter
from app.schemas import (
    ExerciseCreate,
    ExerciseParameterCreate,
    ExerciseParameterUpdate,
    ExerciseUpdate,
)


class CRUDExerciseParameter(
    CRUDBase[ExerciseParameter, ExerciseParameterCreate, ExerciseParameterUpdate]
):
    pass


exercise_parameter = CRUDExerciseParameter(ExerciseParameter)


class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    pass


exercise = CRUDExercise(Exercise)
