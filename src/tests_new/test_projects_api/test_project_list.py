from tests_new.basic_config import client
import pytest


@pytest.mark.parametrize(
    "page, size, filter, expected_status_code",
    [
        (None, None, None, 422),
        (-100, 10, None, 422),
        (1, -100, None, 422),
        (1, 10, None, 200),
        (1, 10, "some text", 200)
    ]
)
def test_project_list(
    page,
    size,
    filter,
    expected_status_code
):
    query_params = {
        "page": page,
        "size": size,
        "filter": filter
    }

    response = client.get(
        "/api/v1/projects",
        params = query_params
    )

    assert response.status_code == expected_status_code