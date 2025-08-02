from tests_new.basic_config import client
import pytest



@pytest.mark.parametrize(
    "project_id, expected_status_code",
    [
        (50, 200),
        (100, 404),
        (-100, 422)
    ]
)
def test_add_role_to_project(
    registered_user_data: dict,
    project_id, 
    expected_status_code
):
    response = client.get(
        f"/api/v1/projects/{project_id}/roles",
        headers = registered_user_data.get("jwt_auth"),
    )

    assert response.status_code == expected_status_code