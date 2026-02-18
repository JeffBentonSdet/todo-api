"""Todo REST serialization schemas. Defines Marshmallow schemas for request validation and response serialization."""

from marshmallow import fields

from todo_api.extensions import ma


class TodoSchema(ma.Schema):
    """Schema for serializing Todo responses."""

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    completed = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CreateTodoSchema(ma.Schema):
    """Schema for validating create todo requests."""

    title = fields.String(required=True)


todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
create_todo_schema = CreateTodoSchema()
