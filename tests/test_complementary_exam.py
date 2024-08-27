from http import HTTPStatus

from tests.conftest import ComplementaryExamFactory, PatientFactory


def test_create_complementary_exam(client, token):
    response = client.post(
        '/complementary-exams/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'patient_id': 1,
            'exam_details': 'complementary_exam exam_details',
        },
    )

    assert response.json() == {
        'exam_id': 1,
        'patient_id': 1,
        'exam_details': 'complementary_exam exam_details',
    }


def test_list_complementary_exams_should_return_5_complementary_exams(session, client, token):
    expected_complementary_exams = 5
    session.bulk_save_objects(
        PatientFactory.create_batch(
            5,
        )
    )
    session.bulk_save_objects(ComplementaryExamFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/complementary-exams/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['complementary_exams']) == expected_complementary_exams


def test_list_complementary_exams_filter_exam_details_should_return_5_complementary_exams(session, client, token):
    expected_complementary_exams = 5
    session.bulk_save_objects(PatientFactory.create_batch(5))
    session.bulk_save_objects(ComplementaryExamFactory.create_batch(5, exam_details='exam_details'))
    session.commit()

    response = client.get(
        '/complementary-exams/?exam_details=exam_details',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['complementary_exams']) == expected_complementary_exams


def test_delete_complementary_exam(session, client, token):
    complementary_exam = ComplementaryExamFactory()
    session.add(complementary_exam)
    session.commit()
    session.refresh(complementary_exam)

    response = client.delete(
        f'/complementary-exams/{complementary_exam.exam_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Complementary Exam has been deleted successfully.'}


def test_delete_complementary_exam_error(client, token):
    response = client.delete(
        '/complementary-exam/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_patch_complementary_exam(session, client, token):
    complementary_exam = ComplementaryExamFactory()

    session.add(complementary_exam)
    session.commit()
    session.refresh(complementary_exam)

    response = client.patch(
        f'/complementary-exams/{complementary_exam.exam_id}',
        json={'exam_details': 'complementary_exam exam_details'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['exam_details'] == 'complementary_exam exam_details'


def test_patch_complementary_exam_error(client, token):
    response = client.patch(
        '/complementary-exams/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found.'}
