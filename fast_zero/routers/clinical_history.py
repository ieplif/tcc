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
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/clinical-history', tags=['clinical-history'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


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

