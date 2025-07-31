from .basic_config import (
    client,
    sync_test_engine as engine,
    Base
)
import logging
from requests import Response
import pytest


def get_registered_users_data(header: dict) -> Response:
    # header = {
    #     "Authorization": f"Bearer {token}"
    # }
    response = client.get(
        "/auth/me",
        headers = header
    )

    logging.info(response.json())
    
    return response


def register_new_test_user(user_creds: dict) -> Response:
    response = client.post(
        "/auth/register",
        json=user_creds
    )

    logging.info(response.json())

    return response


def login_into_user(user_creds: dict) -> Response:
    response = client.post(
        "/auth/login",
        json = user_creds
    )
    
    logging.info(response.json())

    return response


@pytest.fixture(scope="session", autouse=True)
def registered_user_data() -> dict:
    payload = {
        "email": "user@example.com",
        "password": "string"
    }

    login_data = login_into_user(payload)
    if login_data.status_code == 200:
        header = {
            "Authorization": f"Bearer {login_data.json().get('accessToken')}"
        }
        logging.info("new user was successfully logged in")

        user_data = get_registered_users_data(header)

        complete_user_data = {
            "jwt_auth": header,
            **login_data.json(),
            **user_data.json(),
            **payload
            }

        return complete_user_data
    elif login_data.status_code == 401: 
        logging.info(f"there was no {payload.get('email')} user in the database")
        
        register_data = register_new_test_user(payload)
        
        if register_data.status_code == 401:
            Base.metadata.drop_all(engine = engine)
            Base.metadata.create_all(engine = engine)
            register_new_test_user(payload)

        login_data = login_into_user(payload)
        header = {
            "Authorization": f"Bearer {login_data.json().get('accessToken')}"
        }
        user_data = get_registered_users_data(header)

        complete_user_data = {
            "jwt_auth": header,
            **login_data.json(),
            **user_data.json(),
            **payload
            }
        
        return complete_user_data