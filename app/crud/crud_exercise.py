from app.crud.base import CRUDBase
from app.models import ExerciseParameter
from app.schemas import ExerciseParameterCreate, ExerciseParameterUpdate


class CRUDExerciseParameter(
    CRUDBase[ExerciseParameter, ExerciseParameterCreate, ExerciseParameterUpdate]
):
    pass


exercise_parameter = CRUDExerciseParameter(ExerciseParameter)
