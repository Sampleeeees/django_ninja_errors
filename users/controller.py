"""
Test controller.
"""
from django.http import HttpRequest
from ninja_extra import ControllerBase, api_controller

from users.api_errors import NotFoundException, UserDisableException, UserInactiveException
from config.route import route
from users.schemas import UserBaseSchema
from users.models import User
from utils.examples_generator import generate_examples


@api_controller("/users", tags=["Users"])
class UserTestController(ControllerBase):

    @route.get(
        "/{user_id}/",
        response=UserBaseSchema,
        openapi_extra=generate_examples(
            NotFoundException,
            UserDisableException,
            UserInactiveException,
            auth=True
        )
    )
    def get_user_by_id(self, request: HttpRequest, user_id: int) -> User:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFoundException