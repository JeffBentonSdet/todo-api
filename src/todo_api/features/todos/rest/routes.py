"""Todo REST route definitions. Defines Flask routes for CRUD operations on todos, handling HTTP request/response concerns."""

from flask import Blueprint, request

from todo_api.core.exceptions import NotFoundError, ValidationError
from todo_api.features.todos.adapters.sql_repository import SqlTodoRepository
from todo_api.features.todos.rest.schemas import (
    create_todo_schema,
    todo_schema,
    todos_schema,
)
from todo_api.features.todos.service import TodoService

bp = Blueprint("todos", __name__, url_prefix="/api/todos")


def _get_service() -> TodoService:
    return TodoService(repository=SqlTodoRepository())


@bp.errorhandler(NotFoundError)
def handle_not_found(error):
    return {"error": str(error)}, 404


@bp.errorhandler(ValidationError)
def handle_validation(error):
    return {"error": str(error)}, 400


@bp.route("", methods=["GET"])
def list_todos():
    """List all todos."""
    service = _get_service()
    todos = service.list_todos()
    return todos_schema.dump(todos), 200


@bp.route("/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    """Get a single todo by ID."""
    service = _get_service()
    todo = service.get_todo(todo_id)
    return todo_schema.dump(todo), 200


@bp.route("", methods=["POST"])
def create_todo():
    """Create a new todo."""
    data = request.get_json()
    if not data or "title" not in data:
        return {"error": "Request must include a JSON body with a 'title' field"}, 400

    errors = create_todo_schema.validate(data)
    if errors:
        return {"error": errors}, 400

    service = _get_service()
    todo = service.create_todo(data["title"])
    return todo_schema.dump(todo), 201


@bp.route("/<int:todo_id>", methods=["PATCH"])
def toggle_todo(todo_id):
    """Toggle the completed status of a todo."""
    service = _get_service()
    todo = service.toggle_completed(todo_id)
    return todo_schema.dump(todo), 200


@bp.route("/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo."""
    service = _get_service()
    service.delete_todo(todo_id)
    return "", 204
