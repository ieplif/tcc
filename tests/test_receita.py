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
