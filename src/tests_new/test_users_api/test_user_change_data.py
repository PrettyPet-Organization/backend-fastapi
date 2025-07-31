from tests_new.basic_config import client
import logging
import pytest


@pytest.mark.parametrize(
        "email, full_name, bio, preferences, experience, expected_status_code",
        [
            ("userexample.com", "string", "string", "string", "string", 422),
            ("user@example.com", "s", "string", "string", "string", 422),
            ("user@example.com", "string", "s", "string", "string", 201),
            ("user@example.com", "string", "string", "s", "string", 422),
            ("user@example.com", "string", "string", "string", "s", 422),
            ("user@example.com", "", "", "", "", 422),
            ("user@example.com", "some long enough working data", "some new working long-enough data", "new data", "string", 201),
        ]
)
def test_user_put(
    registered_user_data: dict,
    email,
    full_name,
    bio,
    preferences,
    experience,
    expected_status_code
):
    payload = {
        "email": email,
        "full_name": full_name,
        "bio": bio,
        "preferences": preferences,
        "experience": experience
    }
    logging.info(registered_user_data.get("jwt_auth"))
    response = client.put(
        f"/api/v1/users/{registered_user_data.get('id')}",
        headers = registered_user_data.get("jwt_auth"),
        json = payload
    )
    
    assert response.status_code == expected_status_code