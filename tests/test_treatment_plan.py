from tests.conftest import TreatmentPlanFactory


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


def test_list_treatment_plans_should_return_5_treatment_plans(session, client, token):
    expected_treatment_plans = 5
    session.bulk_save_objects(TreatmentPlanFactory.create_batch(5))
    session.commit()

    response = client.get(
        '/treatment-plan/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['treatment_plans']) == expected_treatment_plans


def test_list_treatment_plans_filter_objectives_should_return_5_treatment_plans(session, client, token):
    expected_treatment_plans = 5
    session.bulk_save_objects(TreatmentPlanFactory.create_batch(5, objectives='objectives'))
    session.commit()

    response = client.get(
        '/treatment-plan/?objectives=objectives',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['treatment_plans']) == expected_treatment_plans


def test_list_treatment_plans_filter_procedures_should_return_5_treatment_plans(session, client, token):
    expected_treatment_plans = 5
    session.bulk_save_objects(TreatmentPlanFactory.create_batch(5, procedures='procedures'))
    session.commit()

    response = client.get(
        '/treatment-plan/?procedures=procedures',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['treatment_plans']) == expected_treatment_plans


def test_delete_treatment_plan(session, client, token):
    treatment_plan = TreatmentPlanFactory()
    session.add(treatment_plan)
    session.commit()
    session.refresh(treatment_plan)

    response = client.delete(
        f'/treatment-plan/{treatment_plan.plan_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {'message': 'Treatment plan deleted successfully'}
