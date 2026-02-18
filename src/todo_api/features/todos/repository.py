"""Todo repository port. Defines the Protocol (interface) for todo persistence operations, independent of any specific storage implementation."""

from typing import Protocol

from todo_api.features.todos.domain import Todo


class TodoRepository(Protocol):
    """Port for todo persistence operations."""

    def get_all(self) -> list[Todo]: ...

    def get_by_id(self, todo_id: int) -> Todo | None: ...

    def create(self, todo: Todo) -> Todo: ...

    def update(self, todo: Todo) -> Todo | None: ...

    def delete(self, todo_id: int) -> bool: ...
