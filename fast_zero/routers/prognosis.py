from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_zero.models import Prognosis
from fast_zero.schemas import (
    Message,
    PrognosisFilter,
    PrognosisList,
    PrognosisPublic,
    PrognosisSchema,
    PrognosisUpdate,
)
from fast_zero.security import get_session

router = APIRouter(prefix='/prognosis', tags=['prognosis'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=PrognosisPublic)
def create_physiotherapy_diagnosis(
    prognosis: PrognosisSchema,
    session: T_Session,
):
    db_prognosis = Prognosis(
        patient_id=prognosis.patient_id,
        prognosis_details=prognosis.prognosis_details,
    )

    session.add(db_prognosis)
    session.commit()
    session.refresh(db_prognosis)

    return db_prognosis


@router.get('/', response_model=PrognosisList)
def list_prognosis(
    session: T_Session,
    filters: PrognosisFilter = Depends(),
):
    query = session.query(Prognosis)

    if filters.prognosis_details:
        query = query.filter(Prognosis.prognosis_details.ilike(f'%{filters.prognosis_details}%'))

    prognosis = query.all()

    return {'prognosis': prognosis}


@router.delete('/{prognosis_id}', response_model=Message)
def delete_prognosis(
    prognosis_id: int,
    session: T_Session,
):
    prognosis = session.query(Prognosis).filter_by(prognosis_id=prognosis_id).first()

    if not prognosis:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Prognosis not found.')

    session.delete(prognosis)
    session.commit()

    return {'message': 'Prognosis has been deleted successfully.'}


@router.patch('/{prognosis_id}', response_model=PrognosisPublic)
def update_prognosis(
    prognosis_id: int,
    prognosis: PrognosisUpdate,
    session: T_Session,
):
    db_prognosis = session.query(Prognosis).filter_by(prognosis_id=prognosis_id).first()

    if not db_prognosis:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Prognosis not found.')

    for key, value in prognosis.model_dump(exclude_unset=True).items():
        setattr(db_prognosis, key, value)

    session.add(db_prognosis)
    session.commit()
    session.refresh(db_prognosis)

    return db_prognosis
