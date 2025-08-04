import logging

import pytest

from tests_new.basic_config import client


@pytest.mark.parametrize(
        "id, email, full_name, bio, preferences, experience, expected_status_code",
        [
            (50, "userexample.com", "string", "string", "string", "string", 422),
            (50, "user@example.com", "s", "string", "string", "string", 422),
            (50, "user@example.com", "string", "s", "string", "string", 201),
            (50, "user@example.com", "string", "string", "s", "string", 422),
            (50, "user@example.com", "string", "string", "string", "s", 422),
            (50, "user@example.com", "", "", "", "", 422),
            (50, "user@example.com", "some long enough working data", "some new working long-enough data", "new data", "string", 201),
            (51, "user@example.com", "string", "s", "string", "string", 403),
            (100, "user@example.com", "string", "s", "string", "string", 403),
            (-100, "user@example.com", "string", "s", "string", "string", 422),
            (50, "user@example.com", "string", "string", "string", "string", 201),
        ]
)
def test_user_put(
    registered_user_data: dict,
    id: int,
    email: str,
    full_name: str,
    bio: str,
    preferences: str,
    experience: str,
    expected_status_code: int
) -> None:
    payload = {
        "email": email,
        "full_name": full_name,
        "bio": bio,
        "preferences": preferences,
        "experience": experience
    }
    logging.info(registered_user_data.get("jwt_auth"))
    response = client.put(
        f"/api/v1/users/{id}",
        headers = registered_user_data.get("jwt_auth"),
        json = payload
    )

    assert response.status_code == expected_status_code
