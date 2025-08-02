from core.utils.security import hash_password


new_users_list = [
    {
        "id": 50,
        "email": "user@example.com",
        "password_hash": hash_password("string"),
        "full_name": "string",
        "bio": "string",
        "preferences": "string",
        "experience": "string"
    },
    {
        "id": 51,
        "email": "user2@example.com",
        "password_hash": hash_password("string"),
        "full_name": "string",
        "bio": "string",
        "preferences": "string",
        "experience": "string"
    },
    {
        "id": 52,
        "email": "user3@example.com",
        "password_hash": hash_password("string"),
        "full_name": "string",
        "bio": "string",
        "preferences": "string",
        "experience": "string"
    }
]