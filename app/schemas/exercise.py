from typing import List

from pydantic import BaseModel

from .parameter import ExerciseParameter


class ExerciseBase(BaseModel):
    name: str


class ExerciseCreate(ExerciseBase):
    parameters: List[ExerciseParameter]


class ExerciseUpdate(ExerciseBase):
    name: str | None
    parameters: List[ExerciseParameter] | None


class ExerciseInDBBase(ExerciseBase):
    id: int

    class Config:
        orm_mode = True


class Exercise(ExerciseInDBBase):
    parameters: List[ExerciseParameter]


class ExerciseInDB(ExerciseInDBBase):
    pass
