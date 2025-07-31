import pytest
from fastapi import Depends


def test_existing_user(client, auth_user_data):
    response = client.get(
        f"/api/v1/users/{auth_user_data.get('id')}",
        headers={"Authorization": f"Bearer {auth_user_data.get('token')}"}
    )
    assert response.status_code == 200

def test_non_existing_user(client, auth_user_data):
    response = client.get(
        f"/api/v1/users/{auth_user_data.get('id') + 1}",
        headers={"Authorization": f"Bearer {auth_user_data.get('token')}"}
    )
    assert response.status_code == 404


# class TestPutUser:
#     pass

# class Test