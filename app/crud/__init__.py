from app.models.session import TrainingSession
from app.schemas.session import TrainingSessionCreate, TrainingSessionUpdate

from .base import CRUDBase
from .crud_user import user

__training_session = CRUDBase[
    TrainingSession, TrainingSessionCreate, TrainingSessionUpdate
]
training_session = __training_session(TrainingSession)
