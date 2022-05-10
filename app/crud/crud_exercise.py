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
    pass


exercise_parameter = CRUDExerciseParameter(ExerciseParameter)


class CRUDExercise(CRUDBase[Exercise, ExerciseCreate, ExerciseUpdate]):
    def __get_params(self, db: Session, *, ids: List[int]) -> List[ExerciseParameter]:
        return db.query(ExerciseParameter).filter(ExerciseParameter.id.in_(ids)).all()

    def create(self, db: Session, *, obj_in: ExerciseCreate) -> Exercise:
        obj_in_dict = obj_in.dict(exclude={"parameter_ids"})
        obj_in_dict["parameters"] = self.__get_params(db, ids=obj_in.parameter_ids)
        db_obj = Exercise(**obj_in_dict)
        return super()._save(db, db_obj=db_obj)

    def update(
        self, db: Session, *, db_obj: Exercise, obj_in: ExerciseUpdate
    ) -> Exercise:
        obj_in_dict = obj_in.dict(exclude={"parameter_ids"}, exclude_unset=True)
        if obj_in.parameter_ids is not None:
            db_obj.parameters = self.__get_params(db, ids=obj_in.parameter_ids)

        return super().update(db, db_obj=db_obj, obj_in=obj_in_dict)


exercise = CRUDExercise(Exercise)
