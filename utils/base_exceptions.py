"""
Base api exceptions.
"""
import abc
from ninja.errors import HttpError
from ninja_extra import status
from django.utils.translation import gettext_lazy as _


class BaseHTTPException(HttpError, abc.ABC):
    """
    Base class for HTTP exceptions with enforced structure and OpenAPI example.
    """

    status_code: int = 400

    def __init__(self) -> None:
        """Initialize the exception."""
        super().__init__(status_code=self.status_code, message=self.message)

    @abc.abstractmethod
    def example(self) -> dict:
        """Return an example of the error response for OpenAPI docs."""
        ...


class DefaultHTTPException(BaseHTTPException):
    """
    Default HTTP exception class that supports declarative definition of error,
    message, and field, with optional override via constructor.
    """

    status_code: int = 400
    error: str
    message: str
    field: str | None = None

    def __init__(
        self,
        message: str | None = None,
        field: str | None = None,
    ) -> None:
        """Initialize base exception."""
        self.message = message if message else self.message
        self.field = field if field else self.field
        super().__init__()

    def example(self) -> dict:
        """Return an example of the error response. This is used in the OpenAPI docs."""
        # build details
        details = {
            "field": "string",
            "message": self.message,
        }

        return {
            "summary": self.error,
            "value": {
                "status": self.status_code,
                "error": {
                    "code": self.error,
                    "details": details,
                },
            },
        }


# region: Default auth exceptions

class UnauthorizedException(DefaultHTTPException):
    """Exception raised when the user is not authenticated."""

    error = "UNAUTHORIZED"
    message = _("Credentials were not provided.")
    status_code = status.HTTP_403_FORBIDDEN

class InvalidCredentialsException(DefaultHTTPException):
    """Exception raised when the user provides invalid credentials."""

    error = "LOGIN_BAD_CREDENTIALS"
    message = _("Invalid credentials.")
    status_code = status.HTTP_401_UNAUTHORIZED

# endregion




