from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_zero.models import ClinicalExamination
from fast_zero.schemas import (
    ClinicalExaminationFilter,
    ClinicalExaminationList,
    ClinicalExaminationPublic,
    ClinicalExaminationSchema,
    ClinicalExaminationUpdate,
    Message,
    PatientFilter,
)
from fast_zero.security import get_session

router = APIRouter(prefix='/clinical-examination', tags=['clinical-examination'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentPatient = Annotated[PatientFilter, Depends()]


@router.post('/', response_model=ClinicalExaminationPublic)
def create_clinical_examination(
    clinical_examination: ClinicalExaminationSchema,
    session: T_Session,
):
    db_clinic_examination = ClinicalExamination(
        patient_id=clinical_examination.patient_id,
        exam_details=clinical_examination.exam_details,
    )

    session.add(db_clinic_examination)
    session.commit()
    session.refresh(db_clinic_examination)

    return db_clinic_examination


@router.get('/', response_model=ClinicalExaminationList)
def list_clinical_examinations(
    session: T_Session,
    patient: CurrentPatient,
    filters: ClinicalExaminationFilter = Depends(),
):
    query = session.query(ClinicalExamination)

    if filters.exam_details:
        query = query.filter(ClinicalExamination.exam_details.ilike(f'%{filters.exam_details}%'))

    clinical_examinations = query.all()

    return {'clinical_examinations': clinical_examinations}


@router.delete('/{exam_id}', response_model=Message)
def delete_clinical_examination(
    exam_id: int,
    session: T_Session,
):
    clinical_examination = session.query(ClinicalExamination).filter_by(exam_id=exam_id).first()

    if not clinical_examination:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Exam not found.')

    session.delete(clinical_examination)
    session.commit()

    return {'message': 'Clinical Examination has been deleted successfully.'}


@router.patch('/{exam_id}', response_model=ClinicalExaminationPublic)
def patch_clinical_examination(
    exam_id: int,
    clinical_examination: ClinicalExaminationUpdate,
    session: T_Session,
):
    db_clinical_examination = session.query(ClinicalExamination).filter_by(exam_id=exam_id).first()

    if not db_clinical_examination:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Exam not found.')

    for key, value in clinical_examination.model_dump(exclude_unset=True).items():
        setattr(db_clinical_examination, key, value)

    session.add(db_clinical_examination)
    session.commit()
    session.refresh(db_clinical_examination)

    return db_clinical_examination
