import requests

from tests.conftest import TUTORIALS_BASE_URL


def create_tutorial(title="test1", description="test", published=True):
    payload = {
        "title": title,
        "description": description,
        "published": published
    }

    response = requests.post(TUTORIALS_BASE_URL, json=payload)
    assert response.status_code == 201
    return response


def test_create_tutorial(db_connect):
    payload = {
        "title": "test1",
        "description": "test",
        "published": True
    }

    response = requests.post(TUTORIALS_BASE_URL, json=payload)

    data = response.json()

    assert "id" in data
    assert data["title"] == payload["title"]
    tutorial_id = data["id"]

    cur = db_connect["cursor"]

    cur.execute(
        "SELECT title FROM tutorials_tutorial WHERE id = %s",
        [tutorial_id]
    )

    result = cur.fetchone()

    assert result is not None
    assert result[0] == payload["title"]


def test_update_tutorial(db_connect):
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
        f"{TUTORIALS_BASE_URL}/{tutorial_id}",
        json=update_payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == tutorial_id
    assert data["title"] == update_payload["title"]
    cur = db_connect["cursor"]

    cur.execute(
        "SELECT title FROM tutorials_tutorial WHERE id = %s",
        [tutorial_id]
    )

    result = cur.fetchone()

    assert result is not None
    assert result[0] == update_payload["title"]


def test_delete_tutorial(db_connect):
    create_response = create_tutorial(
        title="test1",
        description="test",
        published=True
    )

    tutorial_id = create_response.json()["id"]

    response = requests.delete(f"{TUTORIALS_BASE_URL}/{tutorial_id}")

    assert response.status_code == 204
    cur = db_connect["cursor"]

    cur.execute(
        "SELECT title FROM tutorials_tutorial WHERE id = %s",
        [tutorial_id]
    )

    result = cur.fetchall()

    assert not result


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

    response = requests.get(TUTORIALS_BASE_URL)

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

    response = requests.get(f"{TUTORIALS_BASE_URL}/{tutorial_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == tutorial_id
    assert data["title"] == created_tutorial["title"]