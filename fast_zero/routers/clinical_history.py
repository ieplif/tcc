from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import ClinicalHistory, User
from fast_zero.schemas import (
    ClinicalHistoryFilter,
    ClinicalHistoryList,
    ClinicalHistoryPublic,
    ClinicalHistorySchema,
    PatientFilter,
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/clinical-history', tags=['clinical-history'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentPatient = Annotated[PatientFilter, Depends()]


@router.post('/', response_model=ClinicalHistoryPublic)
def create_clinical_history(
    clinical_history: ClinicalHistorySchema,
    session: T_Session,
    user: CurrentUser,
):
    db_clinical_history = ClinicalHistory(
        patient_id=clinical_history.patient_id,
        main_complaint=clinical_history.main_complaint,
        disease_history=clinical_history.disease_history,
        lifestyle_habits=clinical_history.lifestyle_habits,
        previous_treatments=clinical_history.previous_treatments,
        personal_family_history=clinical_history.personal_family_history,
        other_information=clinical_history.other_information,
        user_id=user.id,
    )
    session.add(db_clinical_history)
    session.commit()
    session.refresh(db_clinical_history)

    return db_clinical_history


@router.get('/', response_model=ClinicalHistoryList)
def list_clinical_histories(
    session: T_Session,
    user: CurrentUser,
    patient: CurrentPatient,
    filters: ClinicalHistoryFilter = Depends(),
):
    query = session.query(ClinicalHistory).where(
        ClinicalHistory.user_id == user.id and ClinicalHistory.patient_id == patient.id
    )

    if filters.main_complaint:
        query = query.filter(ClinicalHistory.main_complaint.ilike(f'%{filters.main_complaint}%'))
    if filters.disease_history:
        query = query.filter(ClinicalHistory.disease_history.ilike(f'%{filters.disease_history}%'))
    if filters.lifestyle_habits:
        query = query.filter(ClinicalHistory.lifestyle_habits.ilike(f'%{filters.lifestyle_habits}%'))
    if filters.previous_treatments:
        query = query.filter(ClinicalHistory.previous_treatments.ilike(f'%{filters.previous_treatments}%'))
    if filters.personal_family_history:
        query = query.filter(ClinicalHistory.personal_family_history.ilike(f'%{filters.personal_family_history}%'))
    if filters.other_information:
        query = query.filter(ClinicalHistory.other_information.ilike(f'%{filters.other_information}%'))

    return {'clinical_histories': query.all()}
