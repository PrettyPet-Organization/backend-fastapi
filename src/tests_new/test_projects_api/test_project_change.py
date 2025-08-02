from tests_new.basic_config import client
import pytest


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
    id,
    title,
    description,
    desired_fundraising_amount,
    entry_ticket_price,
    expected_status_code
):

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