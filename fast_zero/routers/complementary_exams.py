from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fast_zero.models import ComplementaryExam
from fast_zero.schemas import (
    ComplementaryExamsFilter,
    ComplementaryExamsList,
    ComplementaryExamsPublic,
    ComplementaryExamsSchema,
    ComplementaryExamsUpdate,
    Message,
)
from fast_zero.security import get_session

router = APIRouter(prefix='/complementary_exams', tags=['complementary_exams'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=ComplementaryExamsPublic)
def create_complementary_exam(
    complementary_exam: ComplementaryExamsSchema,
    session: T_Session,
):
    db_complementary_exam = ComplementaryExam(
        patient_id=complementary_exam.patient_id,
        exam_details=complementary_exam.exam_details,
    )

    session.add(db_complementary_exam)
    session.commit()
    session.refresh(db_complementary_exam)

    return db_complementary_exam


@router.get('/', response_model=ComplementaryExamsList)
def list_complementary_exams(
    session: T_Session,
    filters: ComplementaryExamsFilter = Depends(),
):
    query = session.query(ComplementaryExam)

    if filters.exam_details:
        query = query.filter(ComplementaryExam.exam_details.ilike(f'%{filters.exam_details}%'))

    complementary_exams = query.all()

    return {'complementary_exams': complementary_exams}


@router.delete('/{exam_id}', response_model=Message)
def delete_complementary_exam(
    exam_id: int,
    session: T_Session,
):
    complementary_exam = session.query(ComplementaryExam).filter_by(exam_id=exam_id).first()

    if not complementary_exam:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Exam not found.')

    session.delete(complementary_exam)
    session.commit()

    return {'message': 'Complementary Exam has been deleted successfully.'}


@router.patch('/{exam_id}', response_model=ComplementaryExamsPublic)
def update_complementary_exam(
    exam_id: int,
    complementary_exam: ComplementaryExamsUpdate,
    session: T_Session,
):
    db_complementary_exam = session.query(ComplementaryExam).filter_by(exam_id=exam_id).first()

    if not db_complementary_exam:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Exam not found.')

    for key, value in complementary_exam.model_dump(exclude_unset=True).items():
        setattr(db_complementary_exam, key, value)

    session.add(db_complementary_exam)
    session.commit()
    session.refresh(db_complementary_exam)

    return db_complementary_exam
