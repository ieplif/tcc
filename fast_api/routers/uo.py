from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import UO, User
from fast_api.schemas import Message, UOList, UOPublic, UOSchema, UOUpdate
from fast_api.security import get_current_user

router = APIRouter(prefix='/uos', tags=['uos'])

SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UOPublic)
def create_uo(uo: UOSchema, session: SessionDep, user: UserDep):
    db_UO = UO(codigo=uo.codigo, sigla=uo.sigla, nome=uo.nome, user_id=user.id)

    session.add(db_UO)
    session.commit()
    session.refresh(db_UO)

    return db_UO


@router.get('/', response_model=UOList)
def list_uos(
    session: SessionDep,
    user: UserDep,
):
    query = select(UO).where(UO.user_id == user.id)
    uos = session.scalars(query).all()
    return {'uos': uos}


@router.delete('/{uo_id}', response_model=Message)
def delete_uo(uo_id: int, session: SessionDep, user: UserDep):
    uo = session.scalar(select(UO).where(UO.id == uo_id, UO.user_id == user.id))
    if not uo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='UO not found')

    session.delete(uo)
    session.commit()

    return {'message': 'UO deleted'}


@router.patch('/{uo_id}', response_model=UOPublic)
def patch_uo(uo_id: int, uo: UOUpdate, session: SessionDep, user: UserDep):
    db_uo = session.scalar(select(UO).where(UO.id == uo_id, UO.user_id == user.id))
    if not db_uo:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='UO not found')

    for key, value in uo.model_dump(exclude_unset=True).items():
        setattr(db_uo, key, value)

    session.add(db_uo)
    session.commit()
    session.refresh(db_uo)

    return db_uo
