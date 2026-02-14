# ADR-004: Hexagonal Architecture Within Each Vertical Slice

## Status
Accepted

## Context
Within each vertical slice (see ADR-003), we need a consistent internal structure that keeps business logic decoupled from infrastructure concerns such as web frameworks, databases, and external services. Without clear boundaries, domain logic tends to become entangled with Flask request handling or SQLAlchemy models, making it difficult to test business rules in isolation and painful to swap infrastructure components.

## Decision
Each vertical slice follows **hexagonal architecture** (also known as Ports and Adapters) principles:

1. **Domain logic is framework-agnostic.** Domain models and business rules are plain Python classes and functions with no dependencies on Flask, SQLAlchemy, or other infrastructure libraries. They live in the slice's `domain.py` module.

2. **Ports are defined as Python Protocols.** Ports represent the interfaces that the domain layer requires (driven ports, e.g., a repository for persistence) or exposes (driving ports, e.g., a service interface called by routes). These are defined using `typing.Protocol` (PEP 544) in the slice's `ports.py` module. Protocols enable structural subtyping, meaning adapters satisfy a port by implementing the correct methods without needing to inherit from or explicitly register with the Protocol class.

3. **Adapters implement ports.** Concrete implementations of ports live in the slice's `adapters.py` module. For example, a `SqlAlchemyTodoRepository` adapter implements the `TodoRepository` Protocol. Adapters handle all framework and infrastructure interactions.

4. **Dependency wiring happens at the composition root.** The Application Factory or Blueprint registration code wires adapters to ports, typically through constructor injection. This keeps the domain layer unaware of which adapter is in use.

Example structure within a slice:

```python
# ports.py
from typing import Protocol

class TodoRepository(Protocol):
    def find_by_id(self, todo_id: str) -> Todo | None: ...
    def save(self, todo: Todo) -> Todo: ...

# domain.py
class TodoService:
    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo

    def complete_todo(self, todo_id: str) -> Todo:
        todo = self._repo.find_by_id(todo_id)
        if todo is None:
            raise TodoNotFound(todo_id)
        todo.mark_complete()
        return self._repo.save(todo)

# adapters.py
class SqlAlchemyTodoRepository:
    """Implements TodoRepository Protocol via structural subtyping."""
    def find_by_id(self, todo_id: str) -> Todo | None: ...
    def save(self, todo: Todo) -> Todo: ...
```

## Alternatives Considered
- **Abstract Base Classes (ABCs) for ports**: Using `abc.ABC` and `@abstractmethod` to define port interfaces. ABCs enforce the contract at class definition time (raising `TypeError` if methods are missing), which provides earlier error detection. However, ABCs require explicit inheritance, which couples adapters to the port definition module. Protocols were preferred because they support structural subtyping (duck typing with type checker support), which aligns better with Python idioms and keeps adapters decoupled.
- **No formal port/adapter separation**: Allowing domain logic to directly import and use infrastructure code (e.g., calling SQLAlchemy queries from service classes). This is simpler initially but creates tight coupling that makes unit testing require database fixtures or heavy mocking, and makes swapping infrastructure components (e.g., moving from SQLite to PostgreSQL, or from SQL to an external API) expensive.
- **Full Dependency Injection framework (e.g., dependency-injector)**: Using a DI container to manage the wiring of adapters to ports. While DI containers provide powerful features like scoped lifecycles and auto-wiring, they add a layer of indirection that can be confusing and are not necessary at the current project scale. Simple constructor injection, wired manually at the composition root, is sufficient and more transparent.

## Consequences
- **Positive**: Domain logic can be unit tested with simple in-memory fakes or stubs that satisfy the Protocol, with no need for database fixtures, Flask test clients, or mocking frameworks.
- **Positive**: Infrastructure components can be swapped independently. For example, switching from an in-memory repository to a PostgreSQL-backed repository requires only writing a new adapter and updating the wiring code.
- **Positive**: The domain layer serves as living documentation of business rules, free from infrastructure noise.
- **Positive**: Python's Protocol system makes this pattern feel idiomatic rather than ceremonial. Adapters do not need to declare that they implement a port; they just need to have the right methods.
- **Negative**: More files per slice (domain, ports, adapters) compared to a simpler structure where routes directly call the database. For very simple CRUD features, this can feel like over-engineering. The team should use judgment about when a feature is simple enough to collapse layers.
- **Negative**: Developers must understand the hexagonal architecture pattern. The explicit separation of domain, ports, and adapters may be unfamiliar to those used to framework-centric development (e.g., Flask tutorials that put business logic in route handlers).
