from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.models import ComplementaryExam
from fast_zero.schemas import ComplementaryExamsPublic, ComplementaryExamsSchema
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
