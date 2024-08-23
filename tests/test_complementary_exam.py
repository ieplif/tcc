def test_create_complementary_exam(client, token):
    response = client.post(
        '/complementary_exams/',
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
