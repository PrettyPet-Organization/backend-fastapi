from tests_new.basic_config import client
import pytest



@pytest.mark.parametrize(
        "id_shift, expected_status_code",
        [
            (1, 404),
            (2, 404),
            (3, 404),
            (-100, 422),
            (0, 200)
        ]
)
def test_get_user_skills(
    registered_user_data: dict,
    id_shift,
    expected_status_code
):
    response = client.get(
        f"/api/v1/users/{registered_user_data.get('id') + id_shift}",
        headers = registered_user_data.get("jwt_auth")
    ) 

    assert response.status_code == expected_status_code