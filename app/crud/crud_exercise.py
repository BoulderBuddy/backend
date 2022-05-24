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
    def _get_parameters(self, db: Session, obj_in):
        parameter_ids = [x.id for x in obj_in.parameters]

        params = exercise_parameter.get_multi_by_id(db, ids=parameter_ids)
        if len(params) != len(obj_in.parameters):
            # TODO this does not accurately reflect which parameters do and dont exist
            raise ValueError(f"Parameters don't exist: {parameter_ids}")
        return params

    def create(self, db: Session, *, obj_in: ExerciseCreate) -> Exercise:
        obj_in.parameters = self._get_parameters(db, obj_in)
        db_obj = Exercise(**obj_in.dict())
        return super().save(db, db_obj=db_obj)

    def update(
        self, db: Session, *, db_obj: Exercise, obj_in: ExerciseUpdate
    ) -> Exercise:
        if obj_in.parameters:
            obj_in.parameters = self._get_parameters(db, obj_in)

        return super().update(db, db_obj=db_obj, obj_in=obj_in)


exercise = CRUDExercise(Exercise)
