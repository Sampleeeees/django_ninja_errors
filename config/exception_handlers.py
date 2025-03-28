"""
Django ninja extra exception handlers.
"""

from django.http import HttpRequest, JsonResponse
from django.utils.translation import gettext_lazy as _
from ninja.errors import ValidationError
from ninja_extra import status

from utils.base_exceptions import DefaultHTTPException


def register_exception_handlers(api):
    """
    Register exception handlers for ninja api.
    """

    @api.exception_handler(DefaultHTTPException)
    def http_exception_handler(request: HttpRequest, exc: DefaultHTTPException) -> JsonResponse:
        """
        Handle all http exceptions.
        """
        # prepare default details
        details: dict = {
            "message": exc.message
        }

        if exc.field:
            details["field"] = exc.field

        return JsonResponse(
            status=exc.status_code,
            data={
                "status": exc.status_code,
                "error": {
                    "code": exc.error,
                    "details": details
                }
            }
        )

    @api.exception_handler(ValidationError)
    def validation_exception_handler(request: HttpRequest, exc: ValidationError) -> JsonResponse:
        """
        Handle validation errors.
        """
        # prepare list with errors
        error_list: list = []

        # iterate by each error
        for error in exc.errors:
            # get field from exception
            location: str = "query"
            field: str = error["loc"][0]
            field_full = ".".join(map(str, error["loc"][1:])) if len(error["loc"]) > 1 else None
            message = _(error["msg"])

            # append dict with errors to error list
            error_list.append(
                {
                    "location": location,
                    "field": field,
                    "field_full": field_full,
                    "message": message
                }
            )

        return JsonResponse(
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            data={
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "error": {"code": "VALIDATION_ERROR", "details": error_list},
            }
        )