"""
File with api exceptions.
"""
from utils.base_exceptions import DefaultHTTPException


class NotFoundException(DefaultHTTPException):

    status_code = 404
    error = "USER_NOT_FOUND"
    message = "NOT FOUND"


class UserDisableException(DefaultHTTPException):

    status_code = 400
    error = "USER_DISABLE"
    message = "User have disabled status"


class UserInactiveException(DefaultHTTPException):

    status_code = 400
    error = "USER_INACTIVE"
    message = "User have inactive status"