"""Tests for the SQL todo repository adapter. Verifies CRUD operations against an in-memory database."""

import pytest

from todo_api.features.todos.adapters.sql_repository import SqlTodoRepository
from todo_api.features.todos.domain import Todo


@pytest.fixture
def repo(app):
    """Provide a SqlTodoRepository within an app context."""
    with app.app_context():
        yield SqlTodoRepository()


def test_create_and_get_by_id(repo):
    todo = repo.create(Todo(title="Write tests"))
    assert todo.id is not None
    assert todo.title == "Write tests"
    assert todo.completed is False

    retrieved = repo.get_by_id(todo.id)
    assert retrieved is not None
    assert retrieved.title == "Write tests"


def test_get_all_returns_all_todos(repo):
    repo.create(Todo(title="First"))
    repo.create(Todo(title="Second"))

    todos = repo.get_all()
    assert len(todos) == 2
    assert todos[0].title == "First"
    assert todos[1].title == "Second"


def test_get_all_empty(repo):
    assert repo.get_all() == []


def test_get_by_id_not_found(repo):
    assert repo.get_by_id(999) is None


def test_update(repo):
    todo = repo.create(Todo(title="Original"))
    todo.title = "Updated"
    todo.completed = True

    updated = repo.update(todo)
    assert updated is not None
    assert updated.title == "Updated"
    assert updated.completed is True

    retrieved = repo.get_by_id(todo.id)
    assert retrieved.title == "Updated"


def test_update_not_found(repo):
    result = repo.update(Todo(id=999, title="Ghost"))
    assert result is None


def test_delete(repo):
    todo = repo.create(Todo(title="To delete"))
    assert repo.delete(todo.id) is True
    assert repo.get_by_id(todo.id) is None


def test_delete_not_found(repo):
    assert repo.delete(999) is False
