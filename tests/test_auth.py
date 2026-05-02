import os
from unittest.mock import patch, Mock

import requests

from tests.conftest import USERS_BASE_URL

API_URL = os.getenv("API_URL")
SYSTEM_PASSWORD = os.getenv("SYSTEM_PASSWORD")

@patch("requests.post")
def test_fake_auth(mock_post):
    fake_response = Mock()
    fake_response.status_code = 200

    token = "Bearer QpwL5tke4Pnpja7X4"

    fake_response.json.return_value = {
        "Authorization": token
    }

    mock_post.return_value = fake_response

    auth_payload = {
        "username": "admin",
        "password": SYSTEM_PASSWORD
    }

    auth_response = requests.post(
        f"{API_URL}/auth",
        json=auth_payload
    )

    assert auth_response.status_code == 200

    auth_data = auth_response.json()

    assert "Authorization" in auth_data
    assert auth_data["Authorization"] == token

    response = requests.get(
        USERS_BASE_URL,
        headers=auth_data
    )

    assert response.status_code == 200