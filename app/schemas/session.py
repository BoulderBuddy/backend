from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.db.database import KeyType
from app.types import SetStatus

from .exercise import Exercise, ExerciseParameter

# TODO split into files


class ExerciseParameterValueCreate(BaseModel):
    parameter_id: KeyType
    value: Decimal


class ExerciseParameterValue(BaseModel):
    parameter: ExerciseParameter
    value: Decimal

    class Config:
        orm_mode = True


class SetCreate(BaseModel):
    index: int
    status: SetStatus
    values: list[ExerciseParameterValueCreate]


class Set(BaseModel):
    index: int
    status: SetStatus
    values: list[ExerciseParameterValue]

    class Config:
        orm_mode = True


class ExerciseSetCreate(BaseModel):
    exercise_id: KeyType
    sets: list[SetCreate]


class ExerciseSet(BaseModel):
    exercise: Exercise
    sets: list[Set]

    class Config:
        orm_mode = True


class WorkoutCreate(BaseModel):
    exercises: list[ExerciseSetCreate]


class WorkoutUpdate(BaseModel):
    pass  # TODO


class Workout(BaseModel):
    id: KeyType
    exercises: list[ExerciseSet]

    class Config:
        orm_mode = True


class TrainingSessionBase(BaseModel):
    date: date
    comment: str | None


class TrainingSessionCreate(TrainingSessionBase):
    date: date
    comment: str | None
    user_id: int | None


class TrainingSessionUpdate(TrainingSessionBase):
    date: date | None
    comment: str | None


# Properties shared by models stored in DB
class TrainingSessionInDBBase(TrainingSessionBase):
    id: KeyType
    user_id: int | None

    class Config:
        orm_mode = True


# Properties to return to client
class TrainingSession(TrainingSessionInDBBase):
    pass


class TrainingSessionDetail(TrainingSessionInDBBase):
    workouts: list[Workout]


# Properties properties stored in DB
class TrainingSessionInDB(TrainingSessionInDBBase):
    pass
