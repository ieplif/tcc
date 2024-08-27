from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import (
    auth,
    clinical_examination,
    clinical_history,
    complementary_exams,
    patients,
    physiotherapy_diagnosis,
    prognosis,
    treatment_plan,
    users,
)
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(clinical_history.router)
app.include_router(clinical_examination.router)
app.include_router(complementary_exams.router)
app.include_router(physiotherapy_diagnosis.router)
app.include_router(prognosis.router)
app.include_router(treatment_plan.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
