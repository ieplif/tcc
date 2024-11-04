def test_create_uo(client, token):
    response = client.post(
        '/uo/',
        headers={'Authorization': f'Bearer {token}'},
        json={'codigo': '21010', 'sigla': 'SEPLAG', 'nome': 'Secretaria de Planejamento e Gestão'},
    )

    assert response.json() == {
        'id': 1,
        'codigo': 21010,
        'sigla': 'SEPLAG',
        'nome': 'Secretaria de Planejamento e Gestão',
    }
