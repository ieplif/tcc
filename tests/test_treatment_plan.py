def test_create_treatment_plan(client, token):
    response = client.post(
        '/treatment-plan/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'patient_id': 1,
            'objectives': 'treatment_plan.objectives',
            'probable_sessions': 10,
            'procedures': 'treatment_plan.procedures',
        },
    )

    assert response.json() == {
        'plan_id': 1,
        'patient_id': 1,
        'objectives': 'treatment_plan.objectives',
        'probable_sessions': 10,
        'procedures': 'treatment_plan.procedures',
    }
