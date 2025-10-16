import logging

import pytest
from requests import Response

from .basic_config import client


def get_registered_users_data(headers: dict) -> Response:
    response = client.get("/auth/me", headers=headers)

    logging.info(response.json())

    return response


def register_new_test_user(user_creds: dict) -> Response:
    response = client.post("/auth/register", json=user_creds)

    logging.info(response.json())

    return response


def login_into_user(user_creds: dict) -> Response:
    response = client.post("/auth/login", json=user_creds)

    logging.info(response.json())

    return response


@pytest.fixture(scope="session")
def registered_user_data() -> dict:
    payload = {"email": "user@example.com", "password": "string"}
    auth_data = login_into_user(payload)
    headers = {"Authorization": f"Bearer {auth_data.json().get('accessToken')}"}
    user_data = get_registered_users_data(headers)

    user_creds = {
        "jwt_auth": headers,
        **user_data.json(),
        **payload,
        **auth_data.json(),
    }
    logging.info(user_creds)

    return user_creds
