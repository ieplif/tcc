from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.models import TreatmentPlan
from fast_zero.schemas import (
    PatientFilter,
    TreatmentPlanPublic,
    TreatmentPlanSchema,
)
from fast_zero.security import get_session

router = APIRouter(prefix='/treatment-plan', tags=['treatment-plan'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentPatient = Annotated[PatientFilter, Depends()]


@router.post('/', response_model=TreatmentPlanPublic)
def create_treatment_plan(
    treatment_plan: TreatmentPlanSchema,
    session: T_Session,
):
    db_treatment_plan = TreatmentPlan(
        patient_id=treatment_plan.patient_id,
        objectives=treatment_plan.objectives,
        probable_sessions=treatment_plan.probable_sessions,
        procedures=treatment_plan.procedures,
    )
    session.add(db_treatment_plan)
    session.commit()
    session.refresh(db_treatment_plan)

    return db_treatment_plan
