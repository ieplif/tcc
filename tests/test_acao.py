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
