from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.models import ClinicalExamination, User
from fast_zero.schemas import (
    ClinicalExaminationFilter,
    ClinicalExaminationList,
    ClinicalExaminationPublic,
    ClinicalExaminationSchema,
    PatientFilter,
)
from fast_zero.security import get_current_user, get_session

router = APIRouter(prefix='/clinical-examination', tags=['clinical-examination'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentPatient = Annotated[PatientFilter, Depends()]


@router.post('/', response_model=ClinicalExaminationPublic)
def create_clinical_examination(
    clinical_examination: ClinicalExaminationSchema,
    session: T_Session,
    user: CurrentUser,
):
    db_clinic_examination = ClinicalExamination(
        patient_id=clinical_examination.patient_id,
        exam_details=clinical_examination.exam_details,
        user_id=user.id,
    )

    session.add(db_clinic_examination)
    session.commit()
    session.refresh(db_clinic_examination)

    return db_clinic_examination


@router.get('/', response_model=ClinicalExaminationList)
def list_clinical_examinations(
    session: T_Session,
    user: CurrentUser,
    patient: CurrentPatient,
    filters: ClinicalExaminationFilter = Depends(),
):
    query = session.query(ClinicalExamination).where(
        ClinicalExamination.user_id == user.id and ClinicalExamination.patient_id == patient.id
    )

    if filters.exam_details:
        query = query.filter(ClinicalExamination.exam_details.ilike(f'%{filters.exam_details}%'))

    clinical_examinations = query.all()

    return {'clinical_examinations': clinical_examinations}
