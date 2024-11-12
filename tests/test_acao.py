from http import HTTPStatus

from tests.conftest import AcaoFactory


def test_create_acao(client, token):
    response = client.post(
        '/uos/1/acoes',
        json={
            'codigo_acao': '12345',
            'nome': 'Acao Teste',
            'anexo': 2,
            'dotacao': 100000.0,
            'uo_id': 1,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {
        'id': 1,
        'codigo_acao': 12345,
        'nome': 'Acao Teste',
        'anexo': 2,
        'dotacao': 100000.0,
        'uo_id': 1,
    }


def test_list_acoes_should_return_t_acoes(session, client, token):
    expected_acoes = 5
    session.bulk_save_objects(AcaoFactory.create_batch(5, uo_id=1))
    session.commit()

    response = client.get('/uos/1/acoes', headers={'Authorization': f'Bearer {token}'})
    assert len(response.json()['acoes']) == expected_acoes


def test_delete_acao(session, client, token):
    acao = AcaoFactory(uo_id=1)
    session.add(acao)
    session.commit()
    session.refresh(acao)

    response = client.delete(f'/uos/1/acoes/{acao.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Acao deleted'}


def test_delete_acao_error(client, token):
    response = client.delete(f'/uos/1/acoes/{10}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Acao not found'}
