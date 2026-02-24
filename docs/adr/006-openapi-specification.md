# ADR-006: OpenAPI Specification

## Status

Accepted

## Context

The todo-api exposes a REST interface but lacked a formal, machine-readable API contract. Without one, API consumers (e.g., the todo-web frontend, external integrations, or automated tooling) must infer the contract from source code or ad-hoc documentation. A machine-readable spec enables client SDK generation, interactive documentation, and contract validation.

## Decision

Maintain a static `openapi.yaml` file (OpenAPI 3.0.3) co-located with the application package at `src/todo_api/openapi.yaml`. The spec is served as-is at `GET /api/docs` with `Content-Type: application/yaml`.

**Key choices:**

- **Static file, not code-generated.** The API surface is small and stable. Code-generation libraries (e.g., `apispec`, `flask-smorest`) add complexity and require restructuring routes or adding decorators. A static file is easier to read, review, and keep accurate for this scale.
- **OpenAPI 3.0.3, not 3.1.x.** 3.0.3 has broader tooling support (validators, Swagger UI, code generators) than the newer 3.1 series.
- **Served raw as YAML, not parsed and re-serialised as JSON.** Avoids adding `pyyaml` as a runtime dependency. Clients that require JSON can convert locally; Swagger UI and most tooling accept YAML natively.
- **Endpoint at `/api/docs`.** Consistent with the `/api/` prefix used by REST routes. Returns the spec directly rather than rendering a full Swagger UI, keeping the server dependency-free.

## Alternatives Considered

- **`flask-smorest`** — tightly integrated OpenAPI generation with Marshmallow. Requires migrating route definitions to its `MethodView`-based API, which is a larger change than warranted at this stage.
- **`apispec` + plugins** — annotation-driven generation from existing routes and schemas. Adds runtime dependencies and docstring-based annotations that couple documentation to implementation details.
- **Serving Swagger UI** — embedding the Swagger UI static bundle adds significant weight and a maintenance surface. Consumers can point any Swagger UI instance at `/api/docs` themselves.

## Consequences

- The spec must be updated manually when REST routes change. The GraphQL interface is not covered (it has its own introspection mechanism).
- No new runtime dependencies are introduced.
- External tools (Swagger UI, Postman, code generators) can be pointed at `/api/docs` to interact with or generate clients for the API.
- Contract validation can be added to CI by linting `openapi.yaml` with a tool such as Spectral.
