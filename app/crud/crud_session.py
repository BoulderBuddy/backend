from sqlalchemy.orm import Session

from app import models, schemas

from .base import CRUDBase


class CRUDTrainingSession(
    CRUDBase[
        models.TrainingSession,
        schemas.TrainingSessionCreate,
        schemas.TrainingSessionUpdate,
    ]
):
    def create(
        self, db: Session, *, obj_in: schemas.TrainingSessionUpsert
    ) -> models.TrainingSession:
        db_obj = models.TrainingSession(
            **obj_in.dict(exclude={"workouts", "id", "user"})
        )
        return self.save(db, db_obj=db_obj)


session = CRUDTrainingSession(models.TrainingSession)
