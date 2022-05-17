from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Exercise, ExerciseParameter
from app.schemas import (
    ExerciseCreate,
    ExerciseParameterCreate,
    ExerciseParameterUpdate,
    ExerciseUpdate,
)


class CRUDExerciseParameter(
    CRUDBase[ExerciseParameter, ExerciseParameterCreate, ExerciseParameterUpdate]
):
    def get_multi_by_id(
        self, db: Session, *, ids: List[int]
    ) -> List[ExerciseParameter]:
        return db.query(self.model).filter(self.model.id.in_(ids)).all()


exercise_parameter = CRUDExerciseParameter(ExerciseParameter)


class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    def create(self, db: Session, *, obj_in: ExerciseCreate) -> Exercise:
        obj_in_dict = obj_in.dict()
        obj_in_dict["parameters"] = exercise_parameter.get_multi_by_id(
            db, ids=[x.id for x in obj_in.parameters]
        )
        db_obj = Exercise(**obj_in_dict)
        return super()._save(db, db_obj=db_obj)

    def update(
        self, db: Session, *, db_obj: Exercise, obj_in: ExerciseUpdate
    ) -> Exercise:
        obj_in_dict = obj_in.dict(exclude_unset=True)
        if obj_in.parameters is not None:
            db_obj.parameters = exercise_parameter.get_multi_by_id(
                db, ids=[x.id for x in obj_in.parameters]
            )

        return super().update(db, db_obj=db_obj, obj_in=obj_in_dict)


exercise = CRUDExercise(Exercise)
