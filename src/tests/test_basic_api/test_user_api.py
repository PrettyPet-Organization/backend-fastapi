

# def test_user(client):
#     email = "me@example.com"
#     password = "testpass"

#     client.post(
#         "/auth/register",
#         json={
#             "email": email,
#             "password": password
#         }
#     )

#     login_response = client.post(
#         "/auth/login",
#         json={
#             "email": email,
#             "password": password
#         }
#     )
#     token = login_response.json().get("accessToken")

#     response = client.get(
#         "/api/v1/users/1",
#         headers={
#             "Authorization": f"Bearer {token}"
#         }
#     )
    
#     assert response.json().get("")

    



