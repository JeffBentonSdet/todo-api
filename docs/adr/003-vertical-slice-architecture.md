# ADR-003: Vertical Slice Architecture

## Status
Accepted

## Context
The project needs an organizational structure that scales as features are added without creating tightly coupled layers. Traditional layered architectures (controllers, services, repositories as top-level directories) tend to scatter a single feature's code across many directories, making it difficult to understand, modify, or delete a feature in isolation. We need an approach that groups code by feature rather than by technical concern, while still leveraging Flask's native organizational primitives.

## Decision
We adopted **Vertical Slice Architecture** as the primary organizational approach for the todo-api project. Each feature (e.g., "todos", "users", "tags") is a self-contained slice that owns all of its code: routes, domain logic, persistence, validation, and tests.

This is built on top of Flask's **Application Factory** and **Blueprints** pattern:

- Each feature slice is a Python package containing its own Blueprint.
- The Application Factory (`create_app`) assembles the application by registering each slice's Blueprint.
- Slices are independent and do not import from each other. Cross-cutting concerns (e.g., authentication, error handling) are handled by shared middleware or dedicated Blueprints.

A typical slice directory looks like:

```
src/todo_api/features/todos/
    __init__.py          # Blueprint definition and registration
    routes.py            # REST endpoints
    schema.py            # GraphQL types and resolvers
    domain.py            # Domain models and business logic
    ports.py             # Port interfaces (Protocols)
    adapters.py          # Adapter implementations
    tests/
        test_routes.py
        test_domain.py
```

## Alternatives Considered
- **Traditional Layered Architecture**: Organizing code into `controllers/`, `services/`, `repositories/` top-level directories. This approach is familiar but creates high coupling across features at each layer. Changing a feature requires editing files in multiple directories, and it becomes difficult to reason about the blast radius of changes. Deleting a feature means hunting across every layer.
- **Domain-Driven Design with Bounded Contexts**: Full DDD with bounded contexts, aggregates, and domain events. While the principles of DDD inform our design (especially within each slice), the full DDD organizational structure adds significant complexity that is not warranted for a project of this size. We borrow from DDD selectively within each slice.
- **Modular Monolith (standalone modules with explicit APIs)**: Similar to vertical slices but with formal module boundaries enforced at the import level. This was considered overkill for the current project size, though the vertical slice approach positions us well to adopt stricter module boundaries later if needed.

## Consequences
- **Positive**: A developer working on a feature can find all related code in a single directory. This dramatically reduces the time needed to understand, modify, or extend a feature.
- **Positive**: Features can be added or removed by adding or removing a slice package and its Blueprint registration, with minimal impact on the rest of the codebase.
- **Positive**: Flask Blueprints provide a natural and idiomatic mapping for slices, including URL prefix isolation, per-slice error handlers, and template/static file namespacing.
- **Positive**: Each slice can be tested in isolation, and test files live alongside the code they test.
- **Negative**: Some code duplication may occur across slices (e.g., similar validation patterns or utility functions). This is an acceptable trade-off; shared utilities can be extracted into a `common/` package when duplication becomes burdensome.
- **Negative**: Developers accustomed to layered architectures may need guidance on the slice-based approach. The ADR itself and code reviews serve as onboarding tools.
