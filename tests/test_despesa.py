from http import HTTPStatus

from tests.conftest import DespesaFactory


def test_create_despesa(client, token):
    response = client.post(
        '/acoes/1/despesas',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'grupo_de_gasto': 'Gasto Teste',
            'subelemento': 33901321,
            'descricao': 'Despesa Teste',
            'processo': 'SEI-10004/000234/2024',
            'favorecido': 'Fornecedor Teste',
            'mes': 'Janeiro',
            'valor': 100000.0,
            'acao_id': 1,
        },
    )

    assert response.json() == {
        'id': 1,
        'grupo_de_gasto': 'Gasto Teste',
        'subelemento': 33901321,
        'descricao': 'Despesa Teste',
        'processo': 'SEI-10004/000234/2024',
        'favorecido': 'Fornecedor Teste',
        'mes': 'Janeiro',
        'valor': 100000.0,
        'acao_id': 1,
    }


def test_list_despesas_should_return_t_despesas(session, client, token):
    expected_despesas = 5
    session.bulk_save_objects(DespesaFactory.create_batch(5, acao_id=1))
    session.commit()

    response = client.get('/acoes/1/despesas', headers={'Authorization': f'Bearer {token}'})
    assert len(response.json()['despesas']) == expected_despesas


def test_delete_despesa(session, client, token):
    despesa = DespesaFactory(acao_id=1)
    session.add(despesa)
    session.commit()
    session.refresh(despesa)

    response = client.delete(f'/acoes/1/despesas/{despesa.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Despesa deleted'}


def test_delete_despesa_error(client, token):
    response = client.delete(f'/acoes/1/despesas/{10}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Despesa not found'}


def test_patch_despesa(session, client, token):
    despesa = DespesaFactory(acao_id=1)
    session.add(despesa)
    session.commit()
    session.refresh(despesa)

    response = client.patch(
        f'/acoes/1/despesas/{despesa.id}',
        json={'descricao': 'Despesa de Teste'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['descricao'] == 'Despesa de Teste'


def test_patch_despesa_error(client, token):
    response = client.patch(
        '/acoes/1/despesas/10',
        json={'descricao': 'Despesa Atualizada'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Despesa not found'}
