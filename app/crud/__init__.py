from app.models.workout import Workout
from app.schemas.workout import WorkoutCreate, WorkoutUpdate

from .base import CRUDBase
from .crud_user import user

__workout = CRUDBase[Workout, WorkoutCreate, WorkoutUpdate]
workout = __workout(Workout)
