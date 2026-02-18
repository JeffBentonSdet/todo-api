"""Application-level exception definitions. Defines custom exception classes for domain errors, validation failures, and not-found conditions."""


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: int | str):
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} with id {resource_id} not found")


class ValidationError(Exception):
    """Raised when input fails validation rules."""

    def __init__(self, message: str):
        super().__init__(message)
