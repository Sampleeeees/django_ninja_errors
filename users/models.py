from django.contrib.auth.models import AbstractUser, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """User model."""

    phone = PhoneNumberField(unique=True, null=True, blank=True)
