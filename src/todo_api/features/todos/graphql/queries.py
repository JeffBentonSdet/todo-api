"""Todo GraphQL query definitions. Defines resolver functions for reading and listing todos via GraphQL."""

from ariadne import QueryType

from todo_api.features.todos.adapters.sql_repository import SqlTodoRepository
from todo_api.features.todos.service import TodoService

query = QueryType()


def _get_service() -> TodoService:
    return TodoService(repository=SqlTodoRepository())


@query.field("todos")
def resolve_todos(*_):
    service = _get_service()
    return service.list_todos()


@query.field("todo")
def resolve_todo(*_, id):
    service = _get_service()
    return service.get_todo(int(id))
