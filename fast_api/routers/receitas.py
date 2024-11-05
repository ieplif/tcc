from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import Receita
from fast_api.schemas import ReceitaPublic, ReceitaSchema

router = APIRouter(prefix='/uos', tags=['uos'])

SessionDep = Annotated[Session, Depends(get_session)]


@router.post('/{uo_id}/receitas', response_model=ReceitaPublic)
def create_receita(uo_id: int, receita: ReceitaSchema, session: SessionDep):
    db_receita = Receita(nr=receita.nr, descricao=receita.descricao, valor=receita.valor, mes=receita.mes, uo_id=uo_id)

    session.add(db_receita)
    session.commit()
    session.refresh(db_receita)

    return db_receita
