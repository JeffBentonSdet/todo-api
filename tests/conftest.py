"""Pytest configuration and shared fixtures. Provides test fixtures for the Flask application, test client, and database setup."""

import pytest

from todo_api import create_app
from todo_api.extensions import db as _db


@pytest.fixture
def app():
    """Create a Flask application configured for testing."""
    app = create_app("testing")

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    """Provide a Flask test client."""
    return app.test_client()
