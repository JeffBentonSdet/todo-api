"""Tests for the todo service layer. Verifies use case behavior using mocked repository implementations."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from todo_api.core.exceptions import NotFoundError, ValidationError
from todo_api.features.todos.domain import Todo
from todo_api.features.todos.service import TodoService


@pytest.fixture
def repo():
    """Provide a mocked TodoRepository."""
    return MagicMock()


@pytest.fixture
def service(repo):
    """Provide a TodoService with a mocked repository."""
    return TodoService(repository=repo)


def _make_todo(id=1, title="Test", completed=False):
    now = datetime.now(timezone.utc)
    return Todo(id=id, title=title, completed=completed, created_at=now, updated_at=now)


# list_todos

def test_list_todos(service, repo):
    repo.get_all.return_value = [_make_todo(1, "A"), _make_todo(2, "B")]
    todos = service.list_todos()
    assert len(todos) == 2
    repo.get_all.assert_called_once()


def test_list_todos_empty(service, repo):
    repo.get_all.return_value = []
    assert service.list_todos() == []


# get_todo

def test_get_todo(service, repo):
    todo = _make_todo()
    repo.get_by_id.return_value = todo
    result = service.get_todo(1)
    assert result.title == "Test"
    repo.get_by_id.assert_called_once_with(1)


def test_get_todo_not_found(service, repo):
    repo.get_by_id.return_value = None
    with pytest.raises(NotFoundError):
        service.get_todo(999)


# create_todo

def test_create_todo(service, repo):
    repo.create.return_value = _make_todo(title="New todo")
    result = service.create_todo("New todo")
    assert result.title == "New todo"
    repo.create.assert_called_once()
    created_todo = repo.create.call_args[0][0]
    assert created_todo.title == "New todo"


def test_create_todo_strips_whitespace(service, repo):
    repo.create.return_value = _make_todo(title="Trimmed")
    service.create_todo("  Trimmed  ")
    created_todo = repo.create.call_args[0][0]
    assert created_todo.title == "Trimmed"


def test_create_todo_blank_title(service, repo):
    with pytest.raises(ValidationError):
        service.create_todo("")


def test_create_todo_whitespace_only_title(service, repo):
    with pytest.raises(ValidationError):
        service.create_todo("   ")


# toggle_completed

def test_toggle_completed(service, repo):
    todo = _make_todo(completed=False)
    toggled = _make_todo(completed=True)
    repo.get_by_id.return_value = todo
    repo.update.return_value = toggled

    result = service.toggle_completed(1)
    assert result.completed is True
    repo.update.assert_called_once()


def test_toggle_completed_not_found(service, repo):
    repo.get_by_id.return_value = None
    with pytest.raises(NotFoundError):
        service.toggle_completed(999)


# delete_todo

def test_delete_todo(service, repo):
    repo.delete.return_value = True
    service.delete_todo(1)
    repo.delete.assert_called_once_with(1)


def test_delete_todo_not_found(service, repo):
    repo.delete.return_value = False
    with pytest.raises(NotFoundError):
        service.delete_todo(999)
