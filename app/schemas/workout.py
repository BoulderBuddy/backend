from pydantic import BaseModel

from app.db import KeyType

from .exercise_set import ExerciseSet, ExerciseSetUpsert


class WorkoutCreate(BaseModel):
    exercises: list[ExerciseSetUpsert]


class WorkoutUpdate(BaseModel):
    pass  # TODO


class Workout(BaseModel):
    id: KeyType
    exercises: list[ExerciseSet]

    class Config:
        orm_mode = True


class WorkoutUpsert(Workout):
    id: KeyType | None
    exercises: list[ExerciseSetUpsert]
