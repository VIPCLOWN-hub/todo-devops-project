import pytest

import app as application


@pytest.fixture
def client(tmp_path):

    test_database = tmp_path / "test.db"

    application.DATABASE = str(test_database)

    application.init_db()

    application.app.config["TESTING"] = True

    with application.app.test_client() as client:
        yield client


def test_home_page(client):

    response = client.get("/")

    assert response.status_code == 200


def test_add_task(client):

    response = client.post(
        "/add",
        data={"title": "Learn Docker"},
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Learn Docker" in response.data


def test_complete_task(client):

    client.post(
        "/add",
        data={"title": "Test Task"}
    )

    response = client.get(
        "/complete/1",
        follow_redirects=True
    )

    assert response.status_code == 200


def test_delete_task(client):

    client.post(
        "/add",
        data={"title": "Delete Me"}
    )

    response = client.get(
        "/delete/1",
        follow_redirects=True
    )

    assert response.status_code == 200

    assert b"Delete Me" not in response.data