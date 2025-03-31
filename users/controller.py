"""
Test controller.
"""
from django.http import HttpRequest
from ninja_extra import ControllerBase, api_controller, status

from users.api_errors import NotFoundException, UserDisableException, UserInactiveException
from config.route import route
from users.schemas import UserBaseSchema, UserCreatedSchema, UserResponseBaseSchema
from users.models import User
from utils.examples_generator import generate_examples


@api_controller("/users", tags=["Users"])
class UserTestController(ControllerBase):

    @route.get(
        "/{user_id}/",
        response_schema=UserResponseBaseSchema,
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


    @route.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_schema=UserCreatedSchema,
        openapi_extra=generate_examples(
            auth=True,
        )
    )
    def create_user(self, request: HttpRequest, user_schema: UserBaseSchema) -> User:
        return User.objects.create(**user_schema.dict())