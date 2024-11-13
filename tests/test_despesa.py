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
