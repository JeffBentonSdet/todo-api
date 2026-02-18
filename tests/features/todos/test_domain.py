"""Tests for the Todo domain entity."""

from datetime import datetime, timezone

from todo_api.features.todos.domain import Todo


def test_todo_defaults():
    todo = Todo(title="Buy groceries")
    assert todo.title == "Buy groceries"
    assert todo.completed is False
    assert todo.id is None
    assert isinstance(todo.created_at, datetime)
    assert todo.created_at.tzinfo == timezone.utc


def test_todo_with_all_fields():
    now = datetime.now(timezone.utc)
    todo = Todo(id=1, title="Test", completed=True, created_at=now, updated_at=now)
    assert todo.id == 1
    assert todo.completed is True
    assert todo.created_at == now
