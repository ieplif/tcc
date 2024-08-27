from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_zero.models import PhysiotherapyDiagosis
from fast_zero.schemas import (
    Message,
    PhysiotherapyDiagnosisFilter,
    PhysiotherapyDiagnosisList,
    PhysiotherapyDiagnosisPublic,
    PhysiotherapyDiagnosisSchema,
    PhysiotherapyDiagnosisUpdate,
)
from fast_zero.security import get_session

router = APIRouter(prefix='/physiotherapy-diagnosis', tags=['physiotherapy-diagnosis'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=PhysiotherapyDiagnosisPublic)
def create_physiotherapy_diagnosis(
    physiotherapy_diagnosis: PhysiotherapyDiagnosisSchema,
    session: T_Session,
):
    db_physiotherapy_diagnosis = PhysiotherapyDiagosis(
        patient_id=physiotherapy_diagnosis.patient_id,
        diagnosis_details=physiotherapy_diagnosis.diagnosis_details,
    )

    session.add(db_physiotherapy_diagnosis)
    session.commit()
    session.refresh(db_physiotherapy_diagnosis)

    return db_physiotherapy_diagnosis


@router.get('/', response_model=PhysiotherapyDiagnosisList)
def list_physiotherapy_diagnosis(
    session: T_Session,
    filters: PhysiotherapyDiagnosisFilter = Depends(),
):
    query = session.query(PhysiotherapyDiagosis)

    if filters.diagnosis_details:
        query = query.filter(PhysiotherapyDiagosis.diagnosis_details.ilike(f'%{filters.diagnosis_details}%'))

    physiotherapy_diagnosis = query.all()

    return {'physiotherapy_diagnosis': physiotherapy_diagnosis}


@router.delete('/{diagnosis_id}', response_model=Message)
def delete_physiotherapy_diagnosis(
    diagnosis_id: int,
    session: T_Session,
):
    physiotherapy_diagnosis = session.query(PhysiotherapyDiagosis).filter_by(diagnosis_id=diagnosis_id).first()

    if not physiotherapy_diagnosis:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Diagnosis not found.')

    session.delete(physiotherapy_diagnosis)
    session.commit()

    return {'message': 'Diagnosis has been deleted successfully.'}


@router.patch('/{diagnosis_id}', response_model=PhysiotherapyDiagnosisPublic)
def update_physiotherapy_diagnosis(
    diagnosis_id: int,
    physiotherapy_diagnosis: PhysiotherapyDiagnosisUpdate,
    session: T_Session,
):
    db_physiotherapy_diagnosis = session.query(PhysiotherapyDiagosis).filter_by(diagnosis_id=diagnosis_id).first()

    if not db_physiotherapy_diagnosis:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Diagnosis not found.')

    for key, value in physiotherapy_diagnosis.model_dump(exclude_unset=True).items():
        setattr(db_physiotherapy_diagnosis, key, value)

    session.add(db_physiotherapy_diagnosis)
    session.commit()
    session.refresh(db_physiotherapy_diagnosis)

    return db_physiotherapy_diagnosis
