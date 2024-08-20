def test_create_patient(client, token):
    response = client.post(
        '/patients',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'full_name': 'Maria Aparecida',
            'age': 58,
            'place_of_birth': 'Rio de Janeiro-RJ',
            'marital_status': 'Casada',
            'gender': 'Feminino',
            'profession': 'Professora',
            'residential_address': 'Rua X, 345, Centro - Rio de Janeiro - RJ',
            'commercial_address': 'Rua Y, 600, Barra da Tijuca - Rio de Janeiro - RJ',
        },
    )
    assert response.json() == {
        'id': 1,
        'full_name': 'Maria Aparecida',
        'age': 58,
        'place_of_birth': 'Rio de Janeiro-RJ',
        'marital_status': 'Casada',
        'gender': 'Feminino',
        'profession': 'Professora',
        'residential_address': 'Rua X, 345, Centro - Rio de Janeiro - RJ',
        'commercial_address': 'Rua Y, 600, Barra da Tijuca - Rio de Janeiro - RJ',
    }
