from decimal import Decimal

from pydantic import BaseModel

from app.db import KeyType

from .parameter import ExerciseParameter


class ExerciseParameterValueUpsert(BaseModel):
    parameter_id: KeyType
    value: Decimal


class ExerciseParameterValue(BaseModel):
    parameter: ExerciseParameter
    value: Decimal

    class Config:
        orm_mode = True
