from datetime import date

from pydantic import BaseModel


class WorkoutBase(BaseModel):
    date: date
    comment: str | None


class WorkoutCreate(WorkoutBase):
    date: date
    comment: str | None
    user_id: int


class WorkoutUpdate(WorkoutBase):
    date: date | None
    comment: str | None


# Properties shared by models stored in DB
class WorkoutInDBBase(WorkoutBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Workout(WorkoutInDBBase):
    pass


# Properties properties stored in DB
class WorkoutInDB(WorkoutInDBBase):
    pass
