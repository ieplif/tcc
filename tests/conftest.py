import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_api.app import app
from fast_api.database import get_session
from fast_api.models import (
    UO,
    Acao,
    Receita,
    User,
    table_registry,
)
from fast_api.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class UOFactory(factory.Factory):
    class Meta:
        model = UO

    codigo = factory.fuzzy.FuzzyInteger(10000, 99999)
    sigla = factory.fuzzy.FuzzyText(length=10)
    nome = factory.fuzzy.FuzzyText(length=100)
    user_id = 1


class ReceitaFactory(factory.Factory):
    class Meta:
        model = Receita

    nr = factory.fuzzy.FuzzyInteger(1000000000, 9999999999)
    descricao = factory.fuzzy.FuzzyText(length=100)
    valor = factory.fuzzy.FuzzyFloat(0, 10000000)
    mes = factory.fuzzy.FuzzyText(length=10)
    uo_id = 1


class AcaoFactory(factory.Factory):
    class Meta:
        model = Acao

    codigo_acao = factory.fuzzy.FuzzyInteger(10000, 99999)
    nome = factory.fuzzy.FuzzyText(length=100)
    anexo = factory.fuzzy.FuzzyInteger(1, 10)
    dotacao = factory.fuzzy.FuzzyFloat(0, 10000000)
    uo_id = 1


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd = 'testtest'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture()
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture()
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
