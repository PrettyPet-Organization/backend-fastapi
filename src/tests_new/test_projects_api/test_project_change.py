from decimal import Decimal

import pytest

from tests_new.basic_config import client


@pytest.mark.parametrize(
    "id, title, description, desired_fundraising_amount, entry_ticket_price, expected_status_code",
    [
        (50, "s", "string", 0, 0, 422),
        (50, "string", "s", 0, 0, 422),
        (50, "string", "string", 0, 0, 201),
        (52, "string", "string", 0, 0, 403),
        (500, "string", "string", 0, 0, 404),
    ]
)
def test_project_put(
    registered_user_data: dict,
    id: int,
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
    response = client.put(
        f"/api/v1/projects/{id}",
        headers = registered_user_data.get("jwt_auth"),
        json = payload
    )

    assert response.status_code == expected_status_code
