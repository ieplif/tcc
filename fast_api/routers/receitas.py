from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import Receita
from fast_api.schemas import Message, ReceitaList, ReceitaPublic, ReceitaSchema, ReceitaUpdate

router = APIRouter(prefix='/uos', tags=['uos'])

SessionDep = Annotated[Session, Depends(get_session)]


@router.post('/{uo_id}/receitas', response_model=ReceitaPublic)
def create_receita(uo_id: int, receita: ReceitaSchema, session: SessionDep):
    db_receita = Receita(nr=receita.nr, descricao=receita.descricao, valor=receita.valor, mes=receita.mes, uo_id=uo_id)

    session.add(db_receita)
    session.commit()
    session.refresh(db_receita)

    return db_receita


@router.get('/{uo_id}/receitas', response_model=ReceitaList)
def list_receitas(uo_id: int, session: SessionDep):
    query = select(Receita).where(Receita.uo_id == uo_id)
    receitas = session.scalars(query).all()
    return {'receitas': receitas}


@router.delete('/{uo_id}/receitas/{receita_id}', response_model=Message)
def delete_receita(uo_id: int, receita_id: int, session: SessionDep):
    receita = session.scalar(select(Receita).where(Receita.id == receita_id, Receita.uo_id == uo_id))
    if not receita:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Receita not found')

    session.delete(receita)
    session.commit()

    return {'message': 'Receita deleted'}


@router.patch('/{uo_id}/receitas/{receita_id}', response_model=ReceitaPublic)
def patch_receita(uo_id: int, receita_id: int, receita: ReceitaUpdate, session: SessionDep):
    db_receita = session.scalar(select(Receita).where(Receita.id == receita_id, Receita.uo_id == uo_id))

    if not db_receita:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Receita not found')

    for key, value in receita.model_dump(exclude_unset=True).items():
        setattr(db_receita, key, value)

    session.add(db_receita)
    session.commit()
    session.refresh(db_receita)

    return db_receita
