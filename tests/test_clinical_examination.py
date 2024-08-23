from http import HTTPStatus

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


def test_list_clinical_examinations_should_return_5_clinical_examinations(session, client, token):
    expected_clinical_examinations = 5
    session.bulk_save_objects(
        PatientFactory.create_batch(
            5,
        )
    )
    session.bulk_save_objects(ClinicalExaminationFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/clinical-examination/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_examinations']) == expected_clinical_examinations


def test_list_clinical_examinations_filter_exam_details_should_return_5_clinical_examinations(session, client, token):
    expected_clinical_examinations = 5
    session.bulk_save_objects(PatientFactory.create_batch(5))
    session.bulk_save_objects(ClinicalExaminationFactory.create_batch(5, exam_details='exam_details'))
    session.commit()

    response = client.get(
        '/clinical-examination/?exam_details=exam_details',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['clinical_examinations']) == expected_clinical_examinations


def test_delete_clinical_examination(session, client, token):
    clinical_examination = ClinicalExaminationFactory()
    session.add(clinical_examination)
    session.commit()
    session.refresh(clinical_examination)

    response = client.delete(
        f'/clinical-examination/{clinical_examination.exam_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Clinical Examination has been deleted successfully.'}


def test_delete_clinical_examination_error(client, token):
    response = client.delete(
        '/clinical-examination/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found.'}


def test_patch_clinical_examination(session, client, token):
    clinical_examination = ClinicalExaminationFactory()

    session.add(clinical_examination)
    session.commit()
    session.refresh(clinical_examination)

    response = client.patch(
        f'/clinical-examination/{clinical_examination.exam_id}',
        json={'exam_details': 'exam_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['exam_details'] == 'exam_details'


def test_patch_clinical_examination_error(client, token):
    response = client.patch(
        '/clinical-examination/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found.'}
