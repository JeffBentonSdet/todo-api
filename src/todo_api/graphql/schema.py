"""Unified GraphQL schema assembly. Composes feature-level queries and mutations into a single executable GraphQL schema."""

from ariadne import make_executable_schema, snake_case_fallback_resolvers

from todo_api.features.todos.graphql import mutation, query, type_defs

# Root type definitions that compose the feature types
root_type_defs = """
    type Query {
        todos: [Todo!]!
        todo(id: ID!): Todo!
    }

    type Mutation {
        createTodo(title: String!): Todo!
        toggleTodo(id: ID!): Todo!
        deleteTodo(id: ID!): DeleteResult!
    }
"""

schema = make_executable_schema(
    [root_type_defs, type_defs],
    query,
    mutation,
    snake_case_fallback_resolvers,
)
