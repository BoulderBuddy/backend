from typing import List

from pydantic import BaseModel


class ExerciseParameterBase(BaseModel):
    name: str


class ExerciseParameterCreate(ExerciseParameterBase):
    pass


class ExerciseParameterUpdate(ExerciseParameterBase):
    name: str | None


# Properties shared by models stored in DB
class ExerciseParameterInDBBase(ExerciseParameterBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class ExerciseParameter(ExerciseParameterInDBBase):
    pass


# Properties properties stored in DB
class ExerciseParameterInDB(ExerciseParameterInDBBase):
    pass


class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    parameter_ids: List[int]


class ExerciseUpdate(ExerciseBase):
    name: str | None
    parameter_ids: List[int] | None


class ExerciseInDBBase(ExerciseBase):
    id: int

    class Config:
        orm_mode = True


class Exercise(ExerciseInDBBase):
    parameter_ids: List[int]

    @classmethod
    def from_orm(cls, obj) -> "Exercise":
        # `obj` is the orm model instance
        if hasattr(obj, "parameters"):
            obj.parameter_ids = [x.id for x in obj.parameters]
            delattr(obj, "parameters")
        return super().from_orm(obj)


class ExerciseInDB(ExerciseInDBBase):
    pass
