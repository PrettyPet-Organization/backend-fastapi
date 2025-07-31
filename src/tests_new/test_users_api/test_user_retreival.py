from tests_new.basic_config import client
import pytest


@pytest.mark.parametrize(
    "id_bias, expected_status_code",
    [
        (0, 200),
        (1, 404),
        (-100, 422)
    ]
)
def test_retreie_correctly(
    registered_user_data: dict,
    id_bias,
    expected_status_code
):
    response = client.get(
        f"/api/v1/users/{registered_user_data.get("id") + id_bias}"
    )

    assert response.status_code == expected_status_code