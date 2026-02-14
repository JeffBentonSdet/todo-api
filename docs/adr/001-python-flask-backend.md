# ADR-001: Python and Flask for Backend Framework

## Status
Accepted

## Context
The todo-api project needs a backend web framework to serve its API. The team requires a framework that is lightweight, well-understood, and flexible enough to support multiple API paradigms (REST and GraphQL) without imposing rigid conventions on project structure. The team has strong Python experience and values a framework that allows explicit architectural decisions rather than enforcing opinionated defaults.

## Decision
We chose **Python** as the programming language and **Flask** as the web framework for the todo-api backend.

Flask's Application Factory pattern and Blueprints system provide the extensibility hooks we need to implement a vertical slice architecture while keeping each slice self-contained. Flask's minimal core means we can layer on exactly the libraries and patterns we need (e.g., Strawberry for GraphQL, SQLAlchemy for persistence) without fighting framework conventions.

Python was selected for its mature ecosystem of libraries for web development, data validation (Pydantic, dataclasses), and testing (pytest), as well as for the team's existing proficiency.

## Alternatives Considered
- **Django / Django REST Framework**: Django provides a batteries-included approach with an ORM, admin panel, and authentication built in. However, its opinionated project structure (apps, models tightly coupled to the ORM) would conflict with our goal of hexagonal architecture and framework-agnostic domain logic. Django's conventions optimize for rapid CRUD development but make it harder to enforce clean separation of concerns.
- **FastAPI**: FastAPI offers excellent performance, automatic OpenAPI documentation, and native async support. It was a strong contender. However, FastAPI's dependency injection system and router model are less amenable to the Blueprint-based vertical slice assembly pattern we wanted. Flask's maturity and the breadth of its extension ecosystem also gave it an edge for our use case.
- **Node.js / Express**: Express shares Flask's minimalist philosophy and would have been a viable choice. It was ruled out primarily because the team's deeper experience is in Python, and Python's type hinting and Protocol system better support our hexagonal architecture goals.

## Consequences
- **Positive**: Flask's simplicity gives us full control over project structure, making it straightforward to implement vertical slice and hexagonal architecture patterns. The Application Factory pattern supports clean configuration and testing. The ecosystem is mature with well-documented extensions.
- **Positive**: Python's Protocol classes (PEP 544) provide a natural way to define ports in our hexagonal architecture without requiring inheritance from abstract base classes.
- **Negative**: Flask is synchronous by default. If the project later requires high-concurrency async workloads, we may need to introduce an ASGI server or adopt Flask's async view support (available since Flask 2.0), which is less battle-tested than FastAPI's native async model.
- **Negative**: Flask requires more manual wiring than a batteries-included framework like Django, meaning more boilerplate for things like request validation and serialization.
