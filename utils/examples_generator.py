"""Examples exception generator."""
from typing import Type
from ninja_extra import status

from utils.base_exceptions import UnauthorizedException, InvalidCredentialsException, DefaultHTTPException


class ExamplesGenerator:
    """Class to generate the examples for the OpenAPI docs."""

    auth_error = (
        UnauthorizedException,
        InvalidCredentialsException,
    )

    @staticmethod
    def generate_nested_schema_for_code(responses, error_code):
        """Generate the nested schema for the given error code."""
        responses[error_code] = {}
        responses[error_code]["content"] = {}
        responses[error_code]["content"]["application/json"] = {}

    @classmethod
    def generate_examples(
        cls,
        *args: Type[DefaultHTTPException],
        auth: bool = False,
    ) -> dict:
        """Generate the error responses for the OpenAPI docs."""
        responses: dict = {}

        if auth:
            args += cls.auth_error

        error_codes = {error.status_code for error in args}

        for error_code in error_codes:
            examples = {}

            for error in args:
                instance = error()  # noqa
                if instance.status_code == error_code:
                    examples[instance.error] = instance.example()

            cls.generate_nested_schema_for_code(responses, error_code)
            responses[error_code]["content"]["application/json"]["examples"] = examples

        cls.validation_error_schema(responses)

        return {"responses": responses}

    @classmethod
    def validation_error_schema(cls, responses):
        """Change the 422 validation schema to match the one used in the API."""
        # check whether there are already errors with 422 status code, if not generate a basic dictionary
        if not responses.get(status.HTTP_422_UNPROCESSABLE_ENTITY):
            cls.generate_nested_schema_for_code(responses, status.HTTP_422_UNPROCESSABLE_ENTITY)

        validation_422_example = {
            "summary": "VALIDATION_ERROR",
            "value": {
                "status": 422,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "details": [
                        {
                            "location": "string",
                            "field": "string",
                            "field_full": "string",
                            "message": "string",
                        }
                    ],
                },
            },
        }
        responses[status.HTTP_422_UNPROCESSABLE_ENTITY]["content"]["application/json"].setdefault("examples", {})[
            "VALIDATION_ERROR"
        ] = validation_422_example


generate_examples = ExamplesGenerator.generate_examples
