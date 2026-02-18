"""GraphQL interface for the todos feature. Exports queries, mutations, and types for the todos feature slice."""

from todo_api.features.todos.graphql.mutations import mutation
from todo_api.features.todos.graphql.queries import query
from todo_api.features.todos.graphql.types import type_defs
