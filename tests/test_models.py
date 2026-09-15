import pytest

from server.models import User, Task


def test_username_model_validation():
    with pytest.raises(ValueError):
        User(
            username="ab",
            email="test@example.com"
        )


def test_email_model_validation():
    user = User(
        username="levi",
        email="test@example.com"
    )

    with pytest.raises(ValueError):
        user.validate_email("email", "invalid-email")


def test_task_title_model_validation():
    task = Task(
        title="Valid title",
        user_id=1
    )

    with pytest.raises(ValueError):
        task.validate_title("title", "   ")


def test_task_completed_model_validation():
    task = Task(
        title="Test task",
        user_id=1
    )

    with pytest.raises(ValueError):
        task.validate_completed("completed", "yes")
