from datetime import date

from pydantic import BaseModel

from app.db import KeyType

from .workout import Workout, WorkoutUpsert


class TrainingSessionBase(BaseModel):
    date: date
    comment: str | None
    user_id: int | None


class TrainingSessionCreate(TrainingSessionBase):
    pass


# TODO deprecate
class TrainingSessionUpdate(TrainingSessionBase):
    date: date | None
    comment: str | None


class TrainingSessionUpsert(TrainingSessionBase):
    id: KeyType | None
    workouts: list[WorkoutUpsert]


class TrainingSessionInDBBase(TrainingSessionBase):
    id: KeyType
    user_id: int | None

    class Config:
        orm_mode = True


class TrainingSession(TrainingSessionInDBBase):
    pass


class TrainingSessionDetail(TrainingSessionInDBBase):
    workouts: list[Workout]
