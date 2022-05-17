from app import crud
from app.crud.crud_exercise import CRUDExercise
from app.models import Exercise
from app.schemas import ExerciseCreate, ExerciseUpdate
from tests.conftest import TestData
from tests.utils import CRUDTestUtil

_default_exercise_data = ExerciseCreate(
    name="Piet", parameters=[TestData.EXER_PARA_1, TestData.EXER_PARA_2]
).__dict__

exercise_crud_util = CRUDTestUtil[
    CRUDExercise, Exercise, ExerciseCreate, ExerciseUpdate
](_default_exercise_data, crud.exercise)
