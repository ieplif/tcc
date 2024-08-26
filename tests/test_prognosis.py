from http import HTTPStatus

from tests.conftest import PatientFactory, PrognosisFactory


def test_create_prognosis(client, token):
    response = client.post(
        '/prognosis/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'patient_id': 1,
            'prognosis_details': 'prognosis prognosis_details',
        },
    )

    assert response.json() == {
        'prognosis_id': 1,
        'patient_id': 1,
        'prognosis_details': 'prognosis prognosis_details',
    }


def test_list_prognosis_should_return_5_prognosis(session, client, token):
    expected_prognosis = 5
    session.bulk_save_objects(
        PatientFactory.create_batch(
            5,
        )
    )
    session.bulk_save_objects(PrognosisFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/prognosis/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['prognosis']) == expected_prognosis


def test_list_prognosis_filter_prognosis_details_should_return_5_prognosis(session, client, token):
    expected_prognosis = 5
    session.bulk_save_objects(PatientFactory.create_batch(5))
    session.bulk_save_objects(PrognosisFactory.create_batch(5, prognosis_details='prognosis_details'))
    session.commit()

    response = client.get(
        '/prognosis/?prognosis_details=prognosis_details',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['prognosis']) == expected_prognosis


def test_delete_prognosis(session, client, token):
    prognosis = PrognosisFactory()
    session.add(prognosis)
    session.commit()
    session.refresh(prognosis)

    response = client.delete(
        f'/prognosis/{prognosis.prognosis_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Prognosis has been deleted successfully.'}


def test_delete_prognosis_error(client, token):
    response = client.delete(
        '/prognosis/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Prognosis not found.'}


def test_patch_prognosis(session, client, token):
    prognosis = PrognosisFactory()

    session.add(prognosis)
    session.commit()
    session.refresh(prognosis)

    response = client.patch(
        f'/prognosis/{prognosis.prognosis_id}',
        json={'prognosis_details': 'prognosis prognosis_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['prognosis_details'] == 'prognosis prognosis_details'


def test_patch_prognosis_error(client, token):
    response = client.patch(
        '/prognosis/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Prognosis not found.'}
