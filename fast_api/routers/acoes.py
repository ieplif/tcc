from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import Acao
from fast_api.schemas import AcaoList, AcaoPublic, AcaoSchema, Message

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


@router.delete('/{uo_id}/acoes/{acao_id}', response_model=Message)
def delete_acao(uo_id: int, acao_id: int, session: SessionDep):
    acao = session.scalar(select(Acao).where(Acao.id == acao_id, Acao.uo_id == uo_id))
    if not acao:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Acao not found')

    session.delete(acao)
    session.commit()

    return {'message': 'Acao deleted'}
