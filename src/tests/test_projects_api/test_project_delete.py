import pytest

from tests.basic_config import client


@pytest.mark.parametrize(
    "id, expected_status_code",
    [
        (51, 204),
        (-100, 422),
        (1000, 404),
        (52, 403)
    ]
)
def test_project_delete(
    registered_user_data: dict,
    id: int,
    expected_status_code: int
) -> None:

    response = client.delete(
        f"/api/v1/projects/{id}",
        headers = registered_user_data.get("jwt_auth")
    )

    assert response.status_code == expected_status_code
