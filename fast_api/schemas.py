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
    receitas: List['ReceitaPublic'] = []
    acoes: List['AcaoPublic'] = []


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


class ReceitaSchema(BaseModel):
    nr: int
    descricao: str
    valor: float
    mes: str
    uo_id: int


class ReceitaPublic(ReceitaSchema):
    id: int


class ReceitaList(BaseModel):
    receitas: list[ReceitaPublic]


class ReceitaFilter(BaseModel):
    nr: int | None = None
    descricao: str | None = None
    valor: float | None = None
    mes: str | None = None
    offset: int | None = None
    limit: int | None = None


class ReceitaUpdate(BaseModel):
    nr: int | None = None
    descricao: str | None = None
    valor: float | None = None
    mes: str | None = None


class AcaoSchema(BaseModel):
    codigo_acao: int
    nome: str
    anexo: int
    dotacao: float
    uo_id: int


class AcaoPublic(AcaoSchema):
    id: int


class AcaoList(BaseModel):
    acoes: list[AcaoPublic]


class AcaoFilter(BaseModel):
    codigo_acao: int | None = None
    nome: str | None = None
    anexo: int | None = None
    dotacao: float | None = None
    uo_id: int | None = None
    offset: int | None = None
    limit: int | None = None


class AcaoUpdate(BaseModel):
    codigo_acao: int | None = None
    nome: str | None = None
    anexo: int | None = None
    dotacao: float | None = None
    uo_id: int | None = None
