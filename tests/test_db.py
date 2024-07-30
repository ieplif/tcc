from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='filiperibeiro',
        email='filipe@email.com',
        password='minhasenha',
    )

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'filipe@email.com')
    )

    assert result.id == 1
