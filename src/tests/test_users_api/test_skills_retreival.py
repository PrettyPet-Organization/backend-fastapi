import logging

import pytest

from tests.basic_config import client


@pytest.mark.parametrize(
        "id, expected_status_code",
        [
            (50, 200),
            (51, 200),
            (52, 200),
            (100, 404),
            (0, 422)
        ]
)
def test_get_user_skills(
    id: int,
    expected_status_code: int
) -> None:
    response = client.get(
        f"/api/v1/users/{id}/skills"
    )

    logging.info(response.json())
    assert response.status_code == expected_status_code
