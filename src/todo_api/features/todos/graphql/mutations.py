"""Todo GraphQL mutation definitions. Defines resolver functions for creating, updating, and deleting todos via GraphQL."""

from ariadne import MutationType

from todo_api.features.todos.adapters.sql_repository import SqlTodoRepository
from todo_api.features.todos.service import TodoService

mutation = MutationType()


def _get_service() -> TodoService:
    return TodoService(repository=SqlTodoRepository())


@mutation.field("createTodo")
def resolve_create_todo(*_, title):
    service = _get_service()
    return service.create_todo(title)


@mutation.field("toggleTodo")
def resolve_toggle_todo(*_, id):
    service = _get_service()
    return service.toggle_completed(int(id))


@mutation.field("deleteTodo")
def resolve_delete_todo(*_, id):
    service = _get_service()
    service.delete_todo(int(id))
    return {"success": True}
