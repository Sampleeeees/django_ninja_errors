"""
File with some schemas for testing.
"""
from utils.django_schema import DjangoSchema


class UserBaseSchema(DjangoSchema):
    """Test schema for user."""

    id: int
    username: str
    first_name: str
