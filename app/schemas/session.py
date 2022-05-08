from datetime import date

from pydantic import BaseModel


class TrainingSessionBase(BaseModel):
    date: date
    comment: str | None


class TrainingSessionCreate(TrainingSessionBase):
    date: date
    comment: str | None
    user_id: int


class TrainingSessionUpdate(TrainingSessionBase):
    date: date | None
    comment: str | None


# Properties shared by models stored in DB
class TrainingSessionInDBBase(TrainingSessionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class TrainingSession(TrainingSessionInDBBase):
    pass


# Properties properties stored in DB
class TrainingSessionInDB(TrainingSessionInDBBase):
    pass
