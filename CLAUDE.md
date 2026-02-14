# Todo API

Python/Flask backend for the todo application, exposing both REST and GraphQL interfaces.

## Tech Stack

- Python with Flask (Application Factory + Blueprints)
- uv for dependency and virtual environment management
- SQLAlchemy for database access
- Marshmallow or Pydantic for serialization/validation

## Commands

```bash
uv sync                  # Install dependencies
uv run flask run         # Start development server
uv run pytest            # Run all tests
uv run pytest tests/features/todos/test_domain.py  # Run a specific test file
```

## Architecture

This project uses **Vertical Slice Architecture** with **hexagonal architecture** within each slice. See `docs/adr/` for detailed rationale.

### Feature Slice Structure

Each feature in `src/todo_api/features/` contains:

- `domain.py` — Entity and value objects (framework-agnostic)
- `repository.py` — Port (Python Protocol) for persistence
- `service.py` — Use cases orchestrating domain + repository
- `rest/` — Flask Blueprint with routes and schemas
- `graphql/` — Queries, mutations, and type definitions
- `adapters/` — Concrete implementations of ports (e.g., SQL repository)

### Key Principles

- Domain logic must not import Flask, SQLAlchemy, or any framework
- Ports are Python Protocols (structural typing), not ABCs
- Adapters implement ports and live in the `adapters/` directory
- REST and GraphQL interfaces both delegate to the same service layer
- The unified GraphQL schema is assembled in `src/todo_api/graphql/schema.py`

## Testing

- Unit tests for domain and service layers use mocked repositories
- REST tests use Flask's test client
- GraphQL tests execute queries against the schema
- Integration tests in `tests/integration/` run against a real database

## Conventions

- All modules include a docstring describing their purpose
- Configuration is loaded from environment variables via `config.py`
- Flask extensions are initialized in `extensions.py` and bound to the app in the factory
