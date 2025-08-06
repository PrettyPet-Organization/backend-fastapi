import pytest

from tests.basic_config import client


@pytest.mark.parametrize(
    "project_id, role_id, description, required_skills_description, number_of_needed, expected_status_code",
    [
        (50, 50, "s", "string", 1, 422),
        (50, 50, "string", "s", 1, 422),
        (52, 50, "string", "string", 1, 403),
        (50, 53, "string", "string", 1, 201),
        (50, 50, "string", "string", 1, 409),
        (50, 500, "string", "string", 1, 404),
    ]
)
def test_add_role_to_project(
    registered_user_data: dict,
    project_id: int,
    role_id: int,
    description: str,
    required_skills_description: str,
    number_of_needed: str,
    expected_status_code: int
) -> None:
    payload = {
        "description": description,
        "required_skills_description": required_skills_description,
        "number_of_needed": number_of_needed
    }
    response = client.post(
        f"/api/v1/projects/{project_id}/roles/{role_id}",
        headers = registered_user_data.get("jwt_auth"),
        json = payload
    )

    assert response.status_code == expected_status_code
