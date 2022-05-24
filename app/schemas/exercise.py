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
