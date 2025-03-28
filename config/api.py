"""
Django ninja extra api configuration.
"""
from ninja_extra import NinjaExtraAPI

from config.exception_handlers import register_exception_handlers
from users.controller import UserTestController

# initialize api
api = NinjaExtraAPI(docs_url="/docs/")

# register custom api exception handling errors
register_exception_handlers(api=api)

# register api controllers
api.register_controllers(
    UserTestController
)
