from enum import Enum, auto

from pydantic import BaseModel

from .parameter_value import ExerciseParameterValue, ExerciseParameterValueUpsert


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class SetStatus(AutoName):
    PLANNED = auto()
    PARTIAL = auto()
    COMPLETE = auto()


class SetUpsert(BaseModel):
    index: int
    status: SetStatus
    values: list[ExerciseParameterValueUpsert]


class Set(BaseModel):
    index: int
    status: SetStatus
    values: list[ExerciseParameterValue]

    class Config:
        orm_mode = True
