import pytest

from tests_new.basic_config import client


@pytest.mark.parametrize(
        "role_id, skill_id, expected_status_code",
        [
            (50, 55, 204),
            (-100, 50, 422),
            (50, 4000, 409),
            (1000, 50, 404),
        ]
)
def test_delete_skill_role_connetcion(
    registered_user_data: dict,
    role_id: int,
    skill_id: int,
    expected_status_code: int
) -> None:
    response = client.delete(
        f"/api/v1/project_roles/{role_id}/skills/{skill_id}",
        headers = registered_user_data.get("jwt_auth")
    )

    assert response.status_code == expected_status_code



