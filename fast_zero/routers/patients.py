from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Patient, User
from fast_zero.schemas import PatientPublic, PatientSchema
from fast_zero.security import get_current_user

router = APIRouter(prefix='/patients', tags=['patients'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=PatientPublic)
def create_patient(
    patient: PatientSchema,
    session: T_Session,
    user: CurrentUser,
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
        user_id=user.id,
    )
    session.add(db_patient)
    session.commit()
    session.refresh(db_patient)

    return db_patient
