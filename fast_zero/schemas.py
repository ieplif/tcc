from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class PatientSchema(BaseModel):
    full_name: str
    age: int
    place_of_birth: str
    marital_status: str
    gender: str
    profession: str
    residential_address: str
    commercial_address: str


class PatientPublic(PatientSchema):
    id: int


class PatientList(BaseModel):
    patients: list[PatientPublic]


class PatientFilter(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    place_of_birth: Optional[str] = None
    marital_status: Optional[str] = None
    gender: Optional[str] = None
    profession: Optional[str] = None
    residential_address: Optional[str] = None
    commercial_address: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    place_of_birth: Optional[str] = None
    marital_status: Optional[str] = None
    gender: Optional[str] = None
    profession: Optional[str] = None
    residential_address: Optional[str] = None
    commercial_address: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
