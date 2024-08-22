from tests.conftest import ClinicalExaminationFactory, PatientFactory


def test_create_clinical_examination(client, token):
    response = client.post(
        '/clinical-examination/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'patient_id': 1,
            'exam_details': 'clinical_examination exam_details',
        },
    )

    assert response.json() == {
        'exam_id': 1,
        'patient_id': 1,
        'exam_details': 'clinical_examination exam_details',
    }


def test_list_clinical_examinations_should_return_5_clinical_examinations(session, client, user, patient, token):
    expected_clinical_examinations = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(ClinicalExaminationFactory.create_batch(5, user_id=user.id, patient_id=patient.id))
    session.commit()

    response = client.get(
        '/clinical-examination/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_examinations']) == expected_clinical_examinations


def test_list_clinical_examinations_filter_exam_details_should_return_5_clinical_examinations(
    session, client, user, patient, token
):
    expected_clinical_examinations = 5
    session.bulk_save_objects(PatientFactory.create_batch(5, user_id=user.id))
    session.bulk_save_objects(
        ClinicalExaminationFactory.create_batch(5, user_id=user.id, patient_id=patient.id, exam_details='exam_details')
    )
    session.commit()

    response = client.get(
        '/clinical-examination/?exam_details=exam_details',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_examinations']) == expected_clinical_examinations
