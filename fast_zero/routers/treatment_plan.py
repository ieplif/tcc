from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_zero.models import TreatmentPlan
from fast_zero.schemas import (
    Message,
    PatientFilter,
    TreatmentPlanFilter,
    TreatmentPlanList,
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


@router.get('/', response_model=TreatmentPlanList)
def list_treatment_plans(
    session: T_Session,
    filters: TreatmentPlanFilter = Depends(),
):
    query = session.query(TreatmentPlan)

    if filters.patient_id:
        query = query.filter(TreatmentPlan.patient_id == filters.patient_id)
    if filters.objectives:
        query = query.filter(TreatmentPlan.objectives.ilike(f'%{filters.objectives}%'))
    if filters.probable_sessions:
        query = query.filter(TreatmentPlan.probable_sessions.ilike(f'%{filters.probable_sessions}%'))
    if filters.procedures:
        query = query.filter(TreatmentPlan.procedures.ilike(f'%{filters.procedures}%'))

    treatment_plans = query.all()

    return {'treatment_plans': treatment_plans}


@router.delete('/{plan_id}', response_model=Message)
def delete_treatment_plan(
    plan_id: int,
    session: T_Session,
):
    treatment_plan = session.query(TreatmentPlan).filter_by(plan_id=plan_id).first()

    if not treatment_plan:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Treatment plan not found')

    session.delete(treatment_plan)
    session.commit()

    return {'message': 'Treatment plan deleted successfully'}
