from unittest.mock import patch, Mock

import requests

from tests.conftest import USERS_BASE_URL


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
        "password": "admin"
    }

    auth_response = requests.post(
        "http://127.0.0.1:8080/api/auth",
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