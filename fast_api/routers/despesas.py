from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import Despesa
from fast_api.schemas import DespesaList, DespesaPublic, DespesaSchema, DespesaUpdate, Message

router = APIRouter(prefix='/acoes', tags=['acoes'])

SessionDep = Annotated[Session, Depends(get_session)]


@router.post('/{acao_id}/despesas', response_model=DespesaPublic)
def create_despesa(acao_id: int, despesa: DespesaSchema, session: SessionDep):
    db_despesa = Despesa(
        grupo_de_gasto=despesa.grupo_de_gasto,
        subelemento=despesa.subelemento,
        descricao=despesa.descricao,
        processo=despesa.processo,
        favorecido=despesa.favorecido,
        mes=despesa.mes,
        valor=despesa.valor,
        acao_id=acao_id,
    )

    session.add(db_despesa)
    session.commit()
    session.refresh(db_despesa)

    return db_despesa


@router.get('/{acao_id}/despesas', response_model=DespesaList)
def list_despesas(acao_id: int, session: SessionDep):
    query = select(Despesa).where(Despesa.acao_id == acao_id)
    despesas = session.scalars(query).all()
    return {'despesas': despesas}


@router.delete('/{acao_id}/despesas/{despesa_id}', response_model=Message)
def delete_despesa(acao_id: int, despesa_id: int, session: SessionDep):
    despesa = session.scalar(select(Despesa).where(Despesa.id == despesa_id, Despesa.acao_id == acao_id))
    if not despesa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Despesa not found')

    session.delete(despesa)
    session.commit()

    return {'message': 'Despesa deleted'}


@router.patch('/{acao_id}/despesas/{despesa_id}', response_model=DespesaPublic)
def patch_despesa(acao_id: int, despesa_id: int, despesa: DespesaUpdate, session: SessionDep):
    db_despesa = session.scalar(select(Despesa).where(Despesa.id == despesa_id, Despesa.acao_id == acao_id))

    if not db_despesa:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Despesa not found')

    for key, value in despesa.model_dump(exclude_unset=True).items():
        setattr(db_despesa, key, value)

    session.add(db_despesa)
    session.commit()
    session.refresh(db_despesa)

    return db_despesa
