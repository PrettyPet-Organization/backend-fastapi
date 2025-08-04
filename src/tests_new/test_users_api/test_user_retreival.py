import pytest

from tests_new.basic_config import client


@pytest.mark.parametrize(
    "id, expected_status_code",
    [
        (-100, 422),
        (50, 200),
        (100, 404)
    ]
)
def test_retreive_correctly(
    id: int,
    expected_status_code: int
) -> None:
    response = client.get(
        f"/api/v1/users/{id}"
    )

    assert response.status_code == expected_status_code
