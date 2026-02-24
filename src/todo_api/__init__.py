"""Todo API application package. Contains the Flask application factory and top-level configuration."""

import os
from pathlib import Path

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

    # Import models so SQLAlchemy registers them before create_all
    import todo_api.features.todos.models  # noqa: F401

    from todo_api.infrastructure.database import init_db
    init_db(app)

    from todo_api.features.todos.rest import bp as todos_bp
    app.register_blueprint(todos_bp)

    from todo_api.graphql import schema
    from ariadne import graphql_sync
    from flask import request, jsonify

    @app.route("/graphql", methods=["POST"])
    def graphql_endpoint():
        data = request.get_json()
        success, result = graphql_sync(schema, data, context_value={"request": request})
        return jsonify(result), 200 if success else 400

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.route("/api/docs")
    def openapi_spec():
        spec_path = Path(app.root_path) / "openapi.yaml"
        return spec_path.read_text(), 200, {"Content-Type": "application/yaml"}

    return app
