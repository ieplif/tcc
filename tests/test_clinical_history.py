from http import HTTPStatus

from tests.conftest import ClinicalHistoryFactory, PatientFactory


def test_create_clinical_history(client, token):
    response = client.post(
        '/clinical-history/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'patient_id': 1,
            'main_complaint': 'clinical_history.main_complaint,',
            'disease_history': 'clinical_history disease_history,',
            'lifestyle_habits': 'clinical_history lifestyle_habits',
            'previous_treatments': 'clinical_history previous_treatments',
            'personal_family_history': 'clinical_history personal_family_history',
            'other_information': 'clinical_history other_information',
        },
    )

    assert response.json() == {
        'history_id': 1,
        'patient_id': 1,
        'main_complaint': 'clinical_history.main_complaint,',
        'disease_history': 'clinical_history disease_history,',
        'lifestyle_habits': 'clinical_history lifestyle_habits',
        'previous_treatments': 'clinical_history previous_treatments',
        'personal_family_history': 'clinical_history personal_family_history',
        'other_information': 'clinical_history other_information',
    }


def test_list_clinical_history_should_return_5_clinical_history(session, client, user, patient, token):
    expected_clinical_histories = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(ClinicalHistoryFactory.create_batch(5, user_id=user.id, patient_id=patient.id))
    session.commit()

    response = client.get(
        '/clinical-history/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_histories']) == expected_clinical_histories


def test_list_clinical_history_filter_main_complaint_should_return_5_clinical_history(
    session, client, user, patient, token
):
    expected_clinical_histories = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(5, user_id=user.id, patient_id=patient.id, main_complaint='main_complaint')
    )
    session.commit()

    response = client.get(
        '/clinical-history/?main_complaint=main_complaint',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_histories']) == expected_clinical_histories


def test_list_clinical_history_filter_disease_history_should_return_5_clinical_history(
    session, client, user, patient, token
):
    expected_clinical_histories = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(
            5, user_id=user.id, patient_id=patient.id, disease_history='disease_history'
        )
    )
    session.commit()

    response = client.get(
        '/clinical-history/?disease_history=disease_history',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_histories']) == expected_clinical_histories


def test_list_clinical_history_filter_lifestyle_habits_should_return_5_clinical_history(
    session, client, user, patient, token
):
    expected_clinical_histories = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(
            5, user_id=user.id, patient_id=patient.id, lifestyle_habits='lifestyle_habits'
        )
    )
    session.commit()

    response = client.get(
        '/clinical-history/?lifestyle_habits=lifestyle_habits',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_histories']) == expected_clinical_histories


def test_list_clinical_history_filter_previous_treatments_should_return_5_clinical_history(
    session, client, user, patient, token
):
    expected_clinical_histories = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(
            5, user_id=user.id, patient_id=patient.id, previous_treatments='previous_treatments'
        )
    )
    session.commit()

    response = client.get(
        '/clinical-history/?previous_treatments=previous_treatments',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_histories']) == expected_clinical_histories


def test_list_clinical_history_filter_personal_family_history_should_return_5_clinical_history(
    session, client, user, patient, token
):
    expected_clinical_histories = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(
            5, user_id=user.id, patient_id=patient.id, personal_family_history='personal_family_history'
        )
    )
    session.commit()

    response = client.get(
        '/clinical-history/?personal_family_history=personal_family_history',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_histories']) == expected_clinical_histories


def test_list_clinical_history_filter_other_information_should_return_5_clinical_history(
    session, client, user, patient, token
):
    expected_clinical_histories = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(
        ClinicalHistoryFactory.create_batch(
            5, user_id=user.id, patient_id=patient.id, other_information='other_information'
        )
    )
    session.commit()

    response = client.get(
        '/clinical-history/?other_information=other_information',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_histories']) == expected_clinical_histories


def test_delete_clinical_history(session, client, user, token):
    clinical_history = ClinicalHistoryFactory(user_id=user.id)
    session.add(clinical_history)
    session.commit()
    session.refresh(clinical_history)

    response = client.delete(
        f'/clinical-history/{clinical_history.history_id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Clinical History has been deleted successfully.'}


def test_delete_clinical_history_error(client, token):
    response = client.delete(f'/clinical-history/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Clinical History not found.'}


def test_patch_clinical_history(session, client, user, token):
    clinical_history = ClinicalHistoryFactory(user_id=user.id)

    session.add(clinical_history)
    session.commit()
    session.refresh(clinical_history)

    response = client.patch(
        f'/clinical-history/{clinical_history.history_id}',
        json={'main_complaint': 'Dor pélvica'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['main_complaint'] == 'Dor pélvica'


def test_patch_clinic_history_error(client, token):
    response = client.patch(
        '/clinical-history/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Clinical History not found.'}
