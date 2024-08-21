from tests.conftest import ClinicalHistoryFactory


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


