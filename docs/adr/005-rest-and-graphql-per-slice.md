# ADR-005: REST and GraphQL Interfaces Per Feature Slice

## Status
Accepted

## Context
The todo-api needs to serve clients with different data-fetching needs. Some consumers (e.g., simple integrations, webhooks, CLI tools) benefit from predictable REST endpoints with standard HTTP semantics. Others (e.g., frontend applications that need to fetch related data in a single request) benefit from GraphQL's flexible query capabilities. Rather than choosing one paradigm exclusively, we want to support both, and we need to decide how to organize the API layer code.

## Decision
Each feature slice exposes **both REST and GraphQL interfaces**:

- **REST routes** are defined in the slice's `routes.py` module and registered as part of the slice's Flask Blueprint. Each slice owns its REST endpoints (e.g., `/api/todos`, `/api/todos/<id>`).
- **GraphQL types and resolvers** are defined in the slice's `schema.py` module using a code-first GraphQL library (e.g., Strawberry). Each slice defines its own GraphQL types, queries, and mutations.
- **At the application level**, the Application Factory collects all slice-level GraphQL schemas and assembles them into a **unified GraphQL schema** served at a single `/graphql` endpoint. This means each slice contributes its types and resolvers independently, but the client sees one cohesive GraphQL API.

Both the REST routes and GraphQL resolvers in a slice call into the same domain layer (via the same ports), ensuring consistent business logic regardless of which API paradigm a client uses.

Example assembly in the Application Factory:

```python
# app.py (Application Factory)
import strawberry
from todo_api.features.todos.schema import TodoQuery, TodoMutation
from todo_api.features.tags.schema import TagQuery, TagMutation

@strawberry.type
class Query(TodoQuery, TagQuery):
    pass

@strawberry.type
class Mutation(TodoMutation, TagMutation):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

## Alternatives Considered
- **REST only**: Providing only REST endpoints and relying on clients to make multiple requests or use query parameters for filtering. This is simpler to implement and sufficient for many use cases, but leads to over-fetching or under-fetching problems for frontend clients that need related data from multiple resources in a single view. Adding REST endpoints for every specific data shape a client needs creates endpoint proliferation.
- **GraphQL only**: Providing only a GraphQL API. While GraphQL can technically serve all use cases, simple integrations (webhooks, CRUD scripts, third-party services expecting REST) become awkward. REST's use of standard HTTP methods and status codes also provides clearer semantics for caching and idempotency. Dropping REST would limit interoperability.
- **Centralized API layer separate from slices**: Defining all REST routes in a single `routes/` directory and all GraphQL schemas in a single `schema/` directory, separate from the feature slices. This contradicts the vertical slice architecture (ADR-003) by scattering feature code across directories. It also creates tight coupling between the centralized API layer and every feature's domain logic.
- **Separate GraphQL service (BFF pattern)**: Running GraphQL as a separate Backend-for-Frontend service that calls into the REST API. This adds network overhead, deployment complexity, and a maintenance burden that is not justified at our current scale.

## Consequences
- **Positive**: Clients can choose the interface that best fits their needs. Frontend applications use GraphQL for flexible, efficient queries; integrations and simple clients use REST for straightforward HTTP interactions.
- **Positive**: Both interfaces share the same domain logic through the same ports, guaranteeing consistent business rules and reducing duplication.
- **Positive**: Each slice fully owns its API surface (both REST and GraphQL), maintaining the benefits of vertical slice architecture. Adding a new feature means adding one slice with both interfaces, not modifying centralized route or schema files.
- **Positive**: The unified GraphQL schema is assembled automatically from slice contributions, so the addition of a new slice's types and resolvers is a small, localized change in the Application Factory.
- **Negative**: Each slice has more surface area to maintain (routes, schema, and their respective tests). For features that are only consumed via one paradigm, the other interface is unnecessary overhead. The team can choose to omit one interface for a slice if there is a clear reason.
- **Negative**: Keeping REST responses and GraphQL types consistent for the same resource requires discipline. Changes to a domain model must be reflected in both the REST serialization and the GraphQL type definition within the slice.
- **Negative**: The unified GraphQL schema assembly uses multiple inheritance on the `Query` and `Mutation` types, which requires that slices do not define conflicting field names. Naming conventions (e.g., prefixing with the feature name) mitigate this risk.
