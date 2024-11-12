from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import Acao
from fast_api.schemas import AcaoList, AcaoPublic, AcaoSchema

router = APIRouter(prefix='/uos', tags=['uos'])

SessionDep = Annotated[Session, Depends(get_session)]


@router.post('/{uo_id}/acoes', response_model=AcaoPublic)
def create_acao(uo_id: int, acao: AcaoSchema, session: SessionDep):
    db_acao = Acao(
        codigo_acao=acao.codigo_acao,
        nome=acao.nome,
        anexo=acao.anexo,
        dotacao=acao.dotacao,
        uo_id=uo_id,
    )

    session.add(db_acao)
    session.commit()
    session.refresh(db_acao)

    return db_acao


@router.get('/{uo_id}/acoes', response_model=AcaoList)
def list_acoes(uo_id: int, session: SessionDep):
    query = select(Acao).where(Acao.uo_id == uo_id)
    acoes = session.scalars(query).all()
    return {'acoes': acoes}
