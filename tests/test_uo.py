from http import HTTPStatus

from tests.conftest import UOFactory


def test_create_uo(client, token):
    response = client.post(
        '/uos/',
        headers={'Authorization': f'Bearer {token}'},
        json={'codigo': '21010', 'sigla': 'SEPLAG', 'nome': 'Secretaria de Planejamento e Gestão'},
    )

    assert response.json() == {
        'id': 1,
        'codigo': 21010,
        'sigla': 'SEPLAG',
        'nome': 'Secretaria de Planejamento e Gestão',
        'receitas': [],
        'acoes': [],
    }


def test_list_uos_should_return_t_uos(session, client, user, token):
    expected_uos = 5
    session.bulk_save_objects(UOFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get('/uos/', headers={'Authorization': f'Bearer {token}'})
    assert len(response.json()['uos']) == expected_uos


def test_delete_uo(session, client, user, token):
    uo = UOFactory(user_id=user.id)
    session.add(uo)
    session.commit()
    session.refresh(uo)

    response = client.delete(f'/uos/{uo.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'UO deleted'}


def test_delete_UO_error(client, token):
    response = client.delete(f'/uos/{10}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'UO not found'}


def test_patch_uo(session, client, user, token):
    uo = UOFactory(user_id=user.id)
    session.add(uo)
    session.commit()
    session.refresh(uo)

    response = client.patch(
        f'/uos/{uo.id}',
        json={'sigla': 'SEFAZ'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['sigla'] == 'SEFAZ'


def test_patch_uo_error(client, token):
    response = client.patch(
        '/uos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'UO not found'}
