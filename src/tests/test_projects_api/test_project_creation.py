from decimal import Decimal

import pytest

from tests.basic_config import client


@pytest.mark.parametrize(
    "title, description, desired_fundraising_amount, entry_ticket_price, expected_status_code",
    [
        ("new_project", "some_description", 0, 0, 201),
        ("new_project", "s", 0, 0, 422),
        ("n", "some_description", 0, 0, 422),
    ]
)
def test_project_creation(
    registered_user_data: dict,
    title: str,
    description: str,
    desired_fundraising_amount: Decimal,
    entry_ticket_price: Decimal,
    expected_status_code: int
) -> None:
    payload = {
        "title": title,
        "description": description,
        "desired_fundraising_amount": desired_fundraising_amount,
        "entry_ticket_price": entry_ticket_price
    }

    response = client.post(
        "/api/v1/projects",
        headers = registered_user_data.get("jwt_auth"),
        json = payload
    )

    assert response.status_code == expected_status_code
