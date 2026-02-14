# ADR-002: uv for Dependency and Virtual Environment Management

## Status
Accepted

## Context
The project needs a tool to manage Python dependencies, virtual environments, and reproducible builds. The Python ecosystem has historically suffered from fragmented tooling for dependency resolution, lock files, and environment management. We need a solution that is fast, reliable, and simple for developers to use day-to-day, while also producing deterministic builds for CI/CD.

## Decision
We chose **uv** as our dependency and virtual environment manager. uv replaces both `pip` and `venv` (or `virtualenv`) with a single, fast tool, and serves as an alternative to Poetry for dependency resolution and lock file management.

Dependencies are declared in `pyproject.toml` following PEP 621, and uv generates a `uv.lock` lock file for reproducible installs. Developers use `uv sync` to install dependencies and `uv run` to execute commands within the managed environment.

## Alternatives Considered
- **pip + venv (manual management)**: The standard library's `venv` module combined with pip is the most basic approach. It lacks a built-in lock file mechanism (requiring a separate `pip-compile` tool or manual `requirements.txt` management), has slow dependency resolution, and offers no unified workflow for environment creation and dependency installation. This approach is error-prone for reproducibility.
- **Poetry**: Poetry provides dependency resolution, lock files, virtual environment management, and packaging in one tool. It was the leading alternative. However, Poetry's dependency resolver is significantly slower than uv's (which is written in Rust), Poetry uses a `poetry.lock` format and `[tool.poetry]` configuration that diverges from PEP 621 standards, and Poetry's virtual environment management can conflict with other tools. Poetry also does not manage Python installations itself.
- **pipenv**: Pipenv combines pip and virtualenv with a `Pipfile`/`Pipfile.lock` workflow. It has a history of slow dependency resolution, stalled maintenance periods, and a non-standard configuration format. It was not considered a serious contender.
- **conda**: Conda is powerful for scientific computing environments but is heavyweight, uses a separate package index, and is not well-suited for pure Python web application projects.

## Consequences
- **Positive**: uv's Rust-based resolver is dramatically faster than pip or Poetry for dependency resolution and installation (often 10-100x faster), significantly improving developer experience and CI pipeline speed.
- **Positive**: uv uses `pyproject.toml` with PEP 621 metadata, aligning with Python packaging standards. This makes the project configuration portable and not locked into a single tool.
- **Positive**: A single tool handles virtual environment creation, dependency installation, lock file generation, and script execution, reducing cognitive overhead for developers.
- **Negative**: uv is newer than Poetry and pip, so some developers may be unfamiliar with it. Onboarding documentation should include uv setup instructions.
- **Negative**: Some third-party tooling and CI templates assume pip or Poetry. We may need to write custom CI steps rather than using pre-built actions, though uv's adoption is growing rapidly and GitHub Actions support is readily available.
