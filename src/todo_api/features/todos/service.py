"""Todo service layer. Implements use cases for todo operations, orchestrating domain logic and repository interactions."""

from todo_api.core.exceptions import NotFoundError, ValidationError
from todo_api.features.todos.domain import Todo
from todo_api.features.todos.repository import TodoRepository


class TodoService:
    """Use cases for todo operations."""

    def __init__(self, repository: TodoRepository):
        self._repository = repository

    def list_todos(self) -> list[Todo]:
        """Return all todos."""
        return self._repository.get_all()

    def get_todo(self, todo_id: int) -> Todo:
        """Return a single todo by ID. Raises NotFoundError if not found."""
        todo = self._repository.get_by_id(todo_id)
        if todo is None:
            raise NotFoundError("Todo", todo_id)
        return todo

    def create_todo(self, title: str) -> Todo:
        """Create a new todo. Raises ValidationError if title is blank."""
        if not title or not title.strip():
            raise ValidationError("Title must not be blank")
        return self._repository.create(Todo(title=title.strip()))

    def toggle_completed(self, todo_id: int) -> Todo:
        """Toggle the completed status of a todo. Raises NotFoundError if not found."""
        todo = self._repository.get_by_id(todo_id)
        if todo is None:
            raise NotFoundError("Todo", todo_id)
        todo.completed = not todo.completed
        updated = self._repository.update(todo)
        if updated is None:
            raise NotFoundError("Todo", todo_id)
        return updated

    def delete_todo(self, todo_id: int) -> None:
        """Delete a todo. Raises NotFoundError if not found."""
        if not self._repository.delete(todo_id):
            raise NotFoundError("Todo", todo_id)
