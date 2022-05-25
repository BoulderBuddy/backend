from pydantic import BaseModel

from app.db import KeyType

from .exercise import Exercise
from .set import Set, SetUpsert


class ExerciseSetUpsert(BaseModel):
    exercise_id: KeyType
    sets: list[SetUpsert]


class ExerciseSet(BaseModel):
    exercise: Exercise
    sets: list[Set]

    class Config:
        orm_mode = True
