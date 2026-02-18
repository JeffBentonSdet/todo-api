"""Database integration tests. Verifies that the Todo model and database tables are created correctly."""

from todo_api.extensions import db
from todo_api.features.todos.models import TodoModel


def test_todo_table_exists(app):
    """Verify the todos table is created on app startup."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        assert "todos" in inspector.get_table_names()


def test_todo_model_roundtrip(app):
    """Verify a TodoModel can be saved and retrieved."""
    with app.app_context():
        todo = TodoModel(title="Integration test todo")
        db.session.add(todo)
        db.session.commit()

        retrieved = db.session.get(TodoModel, todo.id)
        assert retrieved is not None
        assert retrieved.title == "Integration test todo"
        assert retrieved.completed is False
        assert retrieved.created_at is not None
        assert retrieved.updated_at is not None
