import pytest
import requests

BASE_URL = "http://127.0.0.1:8080/api/tutorials"


@pytest.fixture(autouse=True)
def clear_tutorials():
    requests.delete(BASE_URL)


def create_tutorial(title="test1", description="test", published=True):
    payload = {
        "title": title,
        "description": description,
        "published": published
    }

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201
    return response


def test_create_tutorial():
    payload = {
        "title": "test1",
        "description": "test",
        "published": True
    }

    response = requests.post(BASE_URL, json=payload)

    data = response.json()

    assert "id" in data
    assert data["title"] == payload["title"]


def test_update_tutorial():
    create_response = create_tutorial(
        title="test1",
        description="test",
        published=True
    )

    tutorial_id = create_response.json()["id"]

    update_payload = {
        "title": "test_upd",
        "description": "test_upd",
        "published": False
    }

    response = requests.put(
        f"{BASE_URL}/{tutorial_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == tutorial_id
    assert data["title"] == update_payload["title"]


def test_delete_tutorial():
    create_response = create_tutorial(
        title="test1",
        description="test",
        published=True
    )

    tutorial_id = create_response.json()["id"]

    response = requests.delete(f"{BASE_URL}/{tutorial_id}")

    assert response.status_code == 204


def test_get_tutorials():
    create_tutorial(
        title="test2",
        description="test2",
        published=True
    )

    create_tutorial(
        title="test4",
        description="test4",
        published=False
    )

    expected_titles = {"test2", "test4"}

    response = requests.get(BASE_URL)

    assert response.status_code == 200

    data = response.json()

    actual_titles = set()

    for tutorial in data:
        actual_titles.add(tutorial["title"])

    assert actual_titles == expected_titles


def test_get_tutorial():
    create_response = create_tutorial(
        title="test2",
        description="test2",
        published=True
    )

    created_tutorial = create_response.json()
    tutorial_id = created_tutorial["id"]

    response = requests.get(f"{BASE_URL}/{tutorial_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == tutorial_id
    assert data["title"] == created_tutorial["title"]