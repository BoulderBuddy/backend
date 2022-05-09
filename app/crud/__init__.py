from app.models import TrainingSession
from app.schemas import TrainingSessionCreate, TrainingSessionUpdate

from .base import CRUDBase
from .crud_exercise import exercise, exercise_parameter
from .crud_user import user

__training_session = CRUDBase[
    TrainingSession, TrainingSessionCreate, TrainingSessionUpdate
]
training_session = __training_session(TrainingSession)
