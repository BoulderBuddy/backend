from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: str | None
    surname: str | None
    email: EmailStr
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr


# Properties to receive via API on update
class UserUpdate(UserBase):
    email: EmailStr | None


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass
