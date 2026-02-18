"""Todo API application package. Contains the Flask application factory and top-level configuration."""

import os

from flask import Flask

from todo_api.config import configs
from todo_api.extensions import db, ma


def create_app(config_name=None):
    """Create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "development")

    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    db.init_app(app)
    ma.init_app(app)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
