import pytest

from tests_new.basic_config import client


@pytest.mark.parametrize(
    "id, expected_status_code",
    [
        (1, 200),
        (-100, 422),
        (1000, 404)
    ]
)
def test_project_retreival(
    id,
    expected_status_code
):

    response = client.get(
        f"/api/v1/projects/{id}"
    )

    assert response.status_code == expected_status_code
