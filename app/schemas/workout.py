from datetime import datetime

from pydantic import BaseModel


class WorkoutBase(BaseModel):
    date: datetime
    comment: str | None


class WorkoutCreate(WorkoutBase):
    date: datetime
    comment: str | None
    user_id: int


class WorkoutUpdate(WorkoutBase):
    date: datetime
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
