import pytest

from server.app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["JWT_SECRET_KEY"] = "test-secret-key-that-is-at-least-32-bytes-long"

    with app.app_context():
        db.drop_all()
        db.create_all()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()


def register_user(client, username, email, password):
    return client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


def login_user(client, username, password):
    response = client.post(
        "/login",
        json={
            "username": username,
            "password": password
        }
    )

    return response.get_json()["access_token"]


def auth_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }


def test_register_user(client):
    response = register_user(
        client,
        "levi",
        "levi@test.com",
        "password123"
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["user"]["username"] == "levi"
    assert data["user"]["email"] == "levi@test.com"


def test_login_user(client):
    register_user(
        client,
        "levi",
        "levi@test.com",
        "password123"
    )

    response = client.post(
        "/login",
        json={
            "username": "levi",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_protected_route_requires_token(client):
    response = client.get("/tasks")

    assert response.status_code == 401


def test_create_task(client):
    register_user(
        client,
        "levi",
        "levi@test.com",
        "password123"
    )

    token = login_user(
        client,
        "levi",
        "password123"
    )

    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing task creation",
            "completed": False
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "Test Task"
    assert data["user_id"] == 1


def test_get_tasks(client):
    register_user(
        client,
        "levi",
        "levi@test.com",
        "password123"
    )

    token = login_user(
        client,
        "levi",
        "password123"
    )

    client.post(
        "/tasks",
        json={
            "title": "Task One"
        },
        headers=auth_headers(token)
    )

    response = client.get(
        "/tasks?page=1&per_page=10",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["pagination"]["total"] == 1
    assert len(data["tasks"]) == 1


def test_update_task(client):
    register_user(
        client,
        "levi",
        "levi@test.com",
        "password123"
    )

    token = login_user(
        client,
        "levi",
        "password123"
    )

    create_response = client.post(
        "/tasks",
        json={
            "title": "Old Title"
        },
        headers=auth_headers(token)
    )

    task_id = create_response.get_json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "title": "New Title",
            "completed": True
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["title"] == "New Title"
    assert data["completed"] is True


def test_delete_task(client):
    register_user(
        client,
        "levi",
        "levi@test.com",
        "password123"
    )

    token = login_user(
        client,
        "levi",
        "password123"
    )

    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Me"
        },
        headers=auth_headers(token)
    )

    task_id = create_response.get_json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(token)
    )

    assert get_response.status_code == 404


def test_user_cannot_access_another_users_task(client):
    register_user(
        client,
        "user1",
        "user1@test.com",
        "password123"
    )

    token1 = login_user(
        client,
        "user1",
        "password123"
    )

    create_response = client.post(
        "/tasks",
        json={
            "title": "Private Task"
        },
        headers=auth_headers(token1)
    )

    task_id = create_response.get_json()["id"]

    register_user(
        client,
        "user2",
        "user2@test.com",
        "password456"
    )

    token2 = login_user(
        client,
        "user2",
        "password456"
    )

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers(token2)
    )

    assert response.status_code == 404


def test_invalid_task_is_rejected(client):
    register_user(
        client,
        "levi",
        "levi@test.com",
        "password123"
    )

    token = login_user(
        client,
        "levi",
        "password123"
    )

    response = client.post(
        "/tasks",
        json={
            "description": "Missing title"
        },
        headers=auth_headers(token)
    )

    assert response.status_code == 400
