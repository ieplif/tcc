from http import HTTPStatus

from tests.conftest import ReceitaFactory


def test_create_receita(client, token):
    response = client.post(
        '/uos/1/receitas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nr': 1000000000, 'descricao': 'Receita Teste', 'valor': 100000.0, 'mes': 'Janeiro', 'uo_id': 1},
    )

    assert response.json() == {
        'id': 1,
        'nr': 1000000000,
        'descricao': 'Receita Teste',
        'valor': 100000.0,
        'mes': 'Janeiro',
        'uo_id': 1,
    }


def test_list_receitas_should_return_t_receitas(session, client, token):
    expected_receitas = 5
    session.bulk_save_objects(ReceitaFactory.create_batch(5, uo_id=1))
    session.commit()

    response = client.get('/uos/1/receitas', headers={'Authorization': f'Bearer {token}'})
    assert len(response.json()['receitas']) == expected_receitas


def test_delete_receita(session, client, token):
    receita = ReceitaFactory(uo_id=1)
    session.add(receita)
    session.commit()
    session.refresh(receita)

    response = client.delete(f'/uos/1/receitas/{receita.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Receita deleted'}


def test_delete_receita_error(client, token):
    response = client.delete(f'/uos/1/receitas/{10}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Receita not found'}


def test_patch_receita(session, client, token):
    receita = ReceitaFactory(uo_id=1)
    session.add(receita)
    session.commit()
    session.refresh(receita)

    response = client.patch(
        f'/uos/1/receitas/{receita.id}',
        json={'descricao': 'Receita de Teste'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['descricao'] == 'Receita de Teste'


def test_patch_receita_error(client, token):
    response = client.patch(
        '/uos/1/receitas/10',
        json={'descricao': 'Receita Atualizada'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Receita not found'}
