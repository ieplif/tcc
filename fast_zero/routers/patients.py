from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Patient
from fast_zero.schemas import (
    Message,
    PatientFilter,
    PatientList,
    PatientPublic,
    PatientSchema,
    PatientUpdate,
)

router = APIRouter(prefix='/patients', tags=['patients'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=PatientPublic)
def create_patient(
    patient: PatientSchema,
    session: T_Session,
):
    db_patient = Patient(
        full_name=patient.full_name,
        age=patient.age,
        place_of_birth=patient.place_of_birth,
        marital_status=patient.marital_status,
        gender=patient.gender,
        profession=patient.profession,
        residential_address=patient.residential_address,
        commercial_address=patient.commercial_address,
    )
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)

    return db_patient


@router.get('/', response_model=PatientList)
def list_patients(
    session: T_Session,
    filters: PatientFilter = Depends(),
):
    query = session.query(Patient)

    if filters.full_name:
        query = query.filter(Patient.full_name.ilike(f'%{filters.full_name}%'))
    if filters.age:
        query = query.filter(Patient.age == filters.age)
    if filters.place_of_birth:
        query = query.filter(Patient.place_of_birth.ilike(f'%{filters.place_of_birth}%'))
    if filters.marital_status:
        query = query.filter(Patient.marital_status.ilike(f'%{filters.marital_status}%'))
    if filters.gender:
        query = query.filter(Patient.gender.ilike(f'%{filters.gender}%'))
    if filters.profession:
        query = query.filter(Patient.profession.ilike(f'%{filters.profession}%'))
    if filters.residential_address:
        query = query.filter(Patient.residential_address.ilike(f'%{filters.residential_address}%'))
    if filters.commercial_address:
        query = query.filter(Patient.commercial_address.ilike(f'%{filters.commercial_address}%'))

    if filters.offset is not None:
        query = query.offset(filters.offset)
    if filters.limit is not None:
        query = query.limit(filters.limit)

    patients = session.scalars(query.offset(filters.offset).limit(filters.limit)).all()
    return {'patients': patients}


@router.delete('/{patient_id}', response_model=Message)
def delete_patient(patient_id: int, session: T_Session):
    patient = session.scalar(select(Patient).where(Patient.id == patient_id))

    if not patient:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')

    session.delete(patient)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{patient_id}', response_model=PatientPublic)
def patch_patient(patient_id: int, session: T_Session, patient: PatientUpdate):
    db_patient = session.scalar(select(Patient).where(Patient.id == patient_id))

    if not db_patient:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found.')

    for key, value in patient.model_dump(exclude_unset=True).items():
        setattr(db_patient, key, value)

    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)

    return db_patient
