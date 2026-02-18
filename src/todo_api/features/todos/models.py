"""SQLAlchemy model for the Todo entity. Maps the domain Todo to a database table."""

from datetime import datetime, timezone

from todo_api.extensions import db


class TodoModel(db.Model):
    """SQLAlchemy model for the todos table."""

    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<TodoModel id={self.id} title={self.title!r}>"
