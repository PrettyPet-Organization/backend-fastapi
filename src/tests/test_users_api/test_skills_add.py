import pytest

from tests.basic_config import client


@pytest.mark.parametrize(
    "user_id, skill_id, expected_status_code",
    [
        (-100, 50, 422),
        (50, -100, 422),
        (50, 100, 404),
        (100, 50, 403),
        (50, 50, 201),
        (50, 50, 201),
    ],
)
def test_skills_add(
    registered_user_data: dict, user_id: int, skill_id: int, expected_status_code: int
) -> None:
    response = client.post(
        f"/api/v1/users/{user_id}/skills/{skill_id}",
        headers=registered_user_data.get("jwt_auth"),
    )

    assert response.status_code == expected_status_code
