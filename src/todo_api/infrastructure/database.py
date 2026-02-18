"""Database configuration and session management. Sets up SQLAlchemy engine, session factory, and base model class."""

from todo_api.extensions import db


def init_db(app):
    """Create all database tables within the application context."""
    with app.app_context():
        db.create_all()
