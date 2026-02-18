"""SQL-based todo repository adapter. Implements the todo repository port using SQLAlchemy for relational database persistence."""

from todo_api.extensions import db
from todo_api.features.todos.domain import Todo
from todo_api.features.todos.models import TodoModel


class SqlTodoRepository:
    """SQLAlchemy implementation of the TodoRepository port."""

    def get_all(self) -> list[Todo]:
        models = db.session.query(TodoModel).order_by(TodoModel.created_at).all()
        return [self._to_domain(m) for m in models]

    def get_by_id(self, todo_id: int) -> Todo | None:
        model = db.session.get(TodoModel, todo_id)
        if model is None:
            return None
        return self._to_domain(model)

    def create(self, todo: Todo) -> Todo:
        model = TodoModel(title=todo.title, completed=todo.completed)
        db.session.add(model)
        db.session.commit()
        return self._to_domain(model)

    def update(self, todo: Todo) -> Todo | None:
        model = db.session.get(TodoModel, todo.id)
        if model is None:
            return None
        model.title = todo.title
        model.completed = todo.completed
        db.session.commit()
        return self._to_domain(model)

    def delete(self, todo_id: int) -> bool:
        model = db.session.get(TodoModel, todo_id)
        if model is None:
            return False
        db.session.delete(model)
        db.session.commit()
        return True

    @staticmethod
    def _to_domain(model: TodoModel) -> Todo:
        return Todo(
            id=model.id,
            title=model.title,
            completed=model.completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
