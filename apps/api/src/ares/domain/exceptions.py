from __future__ import annotations


class AresError(Exception):
    def __init__(self, message: str, code: str = "internal_error") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundError(AresError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="not_found")

class AuthenticationError(AresError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="authentication_error")

class AuthorizationError(AresError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="authorization_error")

class ValidationError(AresError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="validation_error")

class ConflictError(AresError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="conflict_error")

class RateLimitError(AresError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="rate_limit_error")
