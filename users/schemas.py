"""
File with some schemas for testing.
"""
from utils.django_schema import DjangoSchema

class UserBaseSchema(DjangoSchema):
    """User base schema."""

    username: str
    first_name: str


class UserResponseBaseSchema(UserBaseSchema):
    """Test schema for user."""

    id: int

    @classmethod
    def schema_extra(cls):
        """Example schema with successfully created response."""
        return {
            "example": {
                "id": 99,
                "username": "John Deer",
                "first_name": "John",
            }
        }


class UserCreatedSchema(UserBaseSchema):
    """
    Test schema for user success created.
    """

    message: str = "User created successfully."


    @classmethod
    def schema_extra(cls):
        """Example schema with successfully created response."""
        return {
            "example": {
                "message": "User created successfully.",
                "id": 1,
                "username": "Joan Deer",
                "first_name": "John",
            }
        }

