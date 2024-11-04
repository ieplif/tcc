from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_api.database import get_session
from fast_api.models import UO, User
from fast_api.schemas import UOPublic, UOSchema
from fast_api.security import get_current_user

router = APIRouter(prefix='/uo', tags=['uo'])

SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UOPublic)
def create_uo(uo: UOSchema, session: SessionDep, user: UserDep):
    db_UO = UO(codigo=uo.codigo, sigla=uo.sigla, nome=uo.nome, user_id=user.id)

    session.add(db_UO)
    session.commit()
    session.refresh(db_UO)

    return db_UO
