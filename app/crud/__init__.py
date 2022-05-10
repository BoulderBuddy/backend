from app.models import TrainingSession
from app.schemas import TrainingSessionCreate, TrainingSessionUpdate

from .base import CRUDBase
from .crud_exercise import exercise, exercise_parameter
from .crud_user import user


class CRUDTrainingSession(
    CRUDBase[TrainingSession, TrainingSessionCreate, TrainingSessionUpdate]
):
    pass


training_session = CRUDTrainingSession(TrainingSession)
