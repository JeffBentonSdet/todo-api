"""Todo GraphQL type definitions. Defines the GraphQL SDL for the todos feature."""

type_defs = """
    type Todo {
        id: ID!
        title: String!
        completed: Boolean!
        createdAt: String!
        updatedAt: String!
    }

    type DeleteResult {
        success: Boolean!
    }
"""
