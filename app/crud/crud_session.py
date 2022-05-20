from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.db import KeyType

from .base import CRUDBase


class CRUDTrainingSession(
    CRUDBase[
        models.TrainingSession,
        schemas.TrainingSessionCreate,
        schemas.TrainingSessionUpdate,
    ]
):
    def get(self, db: Session, id: KeyType) -> models.TrainingSession | None:
        return db.query(models.TrainingSession).options(joinedload("*")).get(id)


session = CRUDTrainingSession(models.TrainingSession)
