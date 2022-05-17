from app import crud
from app.crud.crud_exercise import CRUDExerciseParameter
from app.models import ExerciseParameter
from app.schemas import ExerciseParameterCreate, ExerciseParameterUpdate
from tests.utils import CRUDTestUtil

_default_exer_para_data = ExerciseParameterCreate(name="mm").__dict__

exercise_parameter_crud_util = CRUDTestUtil[
    CRUDExerciseParameter,
    ExerciseParameter,
    ExerciseParameterCreate,
    ExerciseParameterUpdate,
](_default_exer_para_data, crud.exercise_parameter)
