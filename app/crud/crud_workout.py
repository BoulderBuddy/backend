from app import models, schemas

from .base import CRUDBase


class CRUDWorkout(
    CRUDBase[models.Workout, schemas.WorkoutCreate, schemas.WorkoutUpdate]
):
    pass
    # "SELECT * FROM exerciseparametervalue EPV LEFT JOIN
    # "set" S WHERE s.workout_id == 1 and EPV.set_id == S.id;"


workout = CRUDWorkout(models.Workout)
