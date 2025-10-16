import pytest

from tests.basic_config import client


@pytest.mark.parametrize(
    "project_id, role_id, expected_status_code",
    [(50, 52, 204), (52, 50, 403), (50, 500, 404), (100, 50, 404), (-100, 50, 422)],
)
def test_delete_role_project_connection(
    registered_user_data: dict, project_id: int, role_id: int, expected_status_code: int
) -> None:
    response = client.delete(
        f"/api/v1/projects/{project_id}/roles/{role_id}",
        headers=registered_user_data.get("jwt_auth"),
    )

    assert response.status_code == expected_status_code
