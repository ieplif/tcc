from http import HTTPStatus

from tests.conftest import PatientFactory


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


def test_list_patients_should_return_5_patients(session, client, user, token):
    expected_patients = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/patients',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['patients']) == expected_patients


def test_list_patients_filter_full_name_should_return_5_patients(session, client, user, token):
    expected_patients = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id, full_name='Maria Aparecida'))
    session.commit()

    response = client.get(
        '/patients/?full_name=Maria Aparecida',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['patients']) == expected_patients


def test_list_patients_filter_age_should_return_5_patients(session, client, user, token):
    expected_patients = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id, age=58))
    session.commit()

    response = client.get(
        '/patients/?age=58',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['patients']) == expected_patients


def test_list_patients_filter_place_of_birth_should_return_5_patients(session, client, user, token):
    expected_patients = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id, place_of_birth='Rio de Janeiro'))
    session.commit()

    response = client.get(
        '/patients/?place_of_birth=Rio',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['patients']) == expected_patients


def test_delete_patient(session, client, user, token):
    patient = PatientFactory(user_id=user.id)
    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.delete(f'/patients/{patient.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully.'}


def test_delete_patient_error(client, token):
    response = client.delete(f'/patients/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_patient(session, client, user, token):
    patient = PatientFactory(user_id=user.id)

    session.add(patient)
    session.commit()
    session.refresh(patient)

    response = client.patch(
        f'/patients/{patient.id}',
        json={'full_name': 'Maria Aparecida'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['full_name'] == 'Maria Aparecida'


def test_patch_patient_error(client, token):
    response = client.patch(
        '/patients/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
