from typing import List

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
    users: List[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class UOSchema(BaseModel):
    codigo: int
    sigla: str
    nome: str


class UOPublic(UOSchema):
    id: int


class UOList(BaseModel):
    uos: list[UOPublic]


class UOFilter(BaseModel):
    codigo: int | None = None
    sigla: str | None = None
    nome: str | None = None
    offset: int | None = None
    limit: int | None = None


class UOUpdate(BaseModel):
    codigo: int | None = None
    sigla: str | None = None
    nome: str | None = None
