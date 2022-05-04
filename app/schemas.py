from datetime import datetime

from pydantic import BaseModel, EmailStr


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


class UserBase(BaseModel):
    first_name: str | None
    surname: str | None
    email: EmailStr | None
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


# Properties to receive via API on update
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    id: int | None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass
