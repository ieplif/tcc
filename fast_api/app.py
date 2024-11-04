from http import HTTPStatus

from fastapi import FastAPI

from fast_api.routers import (
    auth,
    uo,
    users,
)
from fast_api.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(uo.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}
