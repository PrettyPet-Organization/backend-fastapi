# from tests_new.basic_config import client
# import pytest



# @pytest.mark.parametrize(
#         "role_id, skill_id, expected_status_code",
#         [
#             (1, 1, 204),
#             (-100, 1, 422),
#             (1, 4000, 404),
#             (1000, 1, 404)
#         ]
# )
# def test_skill_role_connection(
#     registered_user_data: dict,
#     role_id,
#     skill_id,
#     expected_status_code
# ):
#     response = client.post(
#         f"/api/v1/project_roles/{role_id}/skills/{skill_id}",
#         headers = registered_user_data.get("jwt_auth")
#     )

#     assert response.status_code == expected_status_code
