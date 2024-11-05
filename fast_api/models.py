from datetime import datetime

from sqlalchemy import Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class UO:
    __tablename__ = 'uos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    codigo: Mapped[int] = mapped_column(unique=True)
    sigla: Mapped[str]
    nome: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    receitas = relationship('Receita', back_populates='uo')


@table_registry.mapped_as_dataclass
class Receita:
    __tablename__ = 'receitas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nr: Mapped[int]
    descricao: Mapped[str]
    valor: Mapped[Float] = mapped_column(Float)
    mes: Mapped[str]
    uo_id: Mapped[int] = mapped_column(ForeignKey('uos.id'))
    uo = relationship('UO', back_populates='receitas')
