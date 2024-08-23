from http import HTTPStatus

from tests.conftest import PatientFactory, PhysiotherapyDiagnosisFactory


def test_create_physiotherapy_diagnosis(client, token):
    response = client.post(
        '/physiotherapy_diagnosis/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'patient_id': 1,
            'diagnosis_details': 'physiotherapy_diagnosis diagnosis_details',
        },
    )

    assert response.json() == {
        'diagnosis_id': 1,
        'patient_id': 1,
        'diagnosis_details': 'physiotherapy_diagnosis diagnosis_details',
    }


def test_list_physiotherapy_diagnosis_should_return_5_physiotherapy_diagnosis(session, client, token):
    expected_physiotherapy_diagnosis = 5
    session.bulk_save_objects(
        PatientFactory.create_batch(
            5,
        )
    )
    session.bulk_save_objects(PhysiotherapyDiagnosisFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/physiotherapy_diagnosis/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['physiotherapy_diagnosis']) == expected_physiotherapy_diagnosis


def test_list_physiotherapy_diagnosis_filter_diagnosis_details_should_return_5_physiotherapy_diagnosis(
    session, client, token
):
    expected_physiotherapy_diagnosis = 5
    session.bulk_save_objects(PatientFactory.create_batch(5))
    session.bulk_save_objects(PhysiotherapyDiagnosisFactory.create_batch(5, diagnosis_details='diagnosis_details'))
    session.commit()

    response = client.get(
        '/physiotherapy_diagnosis/?diagnosis_details=diagnosis_details',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['physiotherapy_diagnosis']) == expected_physiotherapy_diagnosis


def test_delete_physiotherapy_diagnosis(session, client, token):
    physiotherapy_diagnosis = PhysiotherapyDiagnosisFactory()
    session.add(physiotherapy_diagnosis)
    session.commit()
    session.refresh(physiotherapy_diagnosis)

    response = client.delete(
        f'/physiotherapy_diagnosis/{physiotherapy_diagnosis.diagnosis_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Diagnosis has been deleted successfully.'}


def test_delete_physiotherapy_diagnosis_error(client, token):
    response = client.delete(
        '/physiotherapy_diagnosis/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Diagnosis not found.'}


def test_patch_physiotherapy_diagnosis(session, client, token):
    physiotherapy_diagnosis = PhysiotherapyDiagnosisFactory()

    session.add(physiotherapy_diagnosis)
    session.commit()
    session.refresh(physiotherapy_diagnosis)

    response = client.patch(
        f'/physiotherapy_diagnosis/{physiotherapy_diagnosis.diagnosis_id}',
        json={'diagnosis_details': 'physiotherapy_diagnosis diagnosis_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['diagnosis_details'] == 'physiotherapy_diagnosis diagnosis_details'


def test_patch_physiotherapy_diagnosis_error(client, token):
    response = client.patch(
        '/physiotherapy_diagnosis/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Diagnosis not found.'}
