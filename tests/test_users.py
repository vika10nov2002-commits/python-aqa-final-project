import pytest
import requests


BASE_URL = "http://127.0.0.1:8080/api/users"


@pytest.fixture(autouse=True)
def clear_users():
    requests.delete(BASE_URL)


def create_user(username="test1", name="test", password="test"):
    payload = {
        "username": username,
        "name": name,
        "password": password
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    return response


def test_create_user():
    payload = {
        "username": "test1",
        "name": "test",
        "password": "test"
    }

    response = requests.post(BASE_URL, json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == payload["username"]
    assert "id" in data


def test_update_user():
    create_response = create_user(
        username="test1",
        name="test",
        password="test"
    )
    user_id = create_response.json()["id"]

    update_payload = {
        "username": "test_upd",
        "name": "test_upd",
        "password": "test_upd"
    }

    response = requests.put(
        f"{BASE_URL}/{user_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == update_payload["username"]
    assert data["id"] == user_id


def test_delete_user():
    create_response = create_user(
        username="test1",
        name="test",
        password="test"
    )

    user_id = create_response.json()["id"]

    response = requests.delete(f"{BASE_URL}/{user_id}")

    assert response.status_code == 204


def test_get_users():


    expected_usernames = {"test2", "test4"}

    for user in expected_usernames:
        create_user(
            username=user,
            name=user,
            password=user
        )

    response = requests.get(BASE_URL)

    assert response.status_code == 200

    data = response.json()

    actual_usernames = set()

    for user in data:
        actual_usernames.add(user["username"])

    assert actual_usernames == expected_usernames


def test_get_user():
    create_response = create_user(
        username="test2",
        name="test2",
        password="test2"
    )

    created_user = create_response.json()
    user_id = created_user["id"]

    response = requests.get(f"{BASE_URL}/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["username"] == created_user["username"]