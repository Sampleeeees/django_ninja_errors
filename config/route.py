"""
Custom Django Ninja Route class with auto by_alias and response_schema mapping.
"""
import typing as t
from ninja.constants import NOT_SET, NOT_SET_TYPE
from ninja.throttling import BaseThrottle
from ninja.types import TCallable
from ninja_extra import status
from ninja_extra.constants import GET, POST, PUT, PATCH, DELETE
from ninja_extra.controllers import Route
from ninja_extra.permissions import BasePermission


class AutoAliasRoute(Route):
    """
    Custom route class that enables:
    - by_alias=True globally for all responses (Pydantic schema aliasing)
    - simplified HTTP method decorators (get, post, etc.)
    - support for response_schema shortcut to define response by status code
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize route and force by_alias to True."""
        super().__init__(*args, **kwargs)

        self.route_params.by_alias = True

    @classmethod
    def _operation(
        cls,
        method: str,
        path: str = "",
        *,
        response: t.Union[t.Any, t.List[t.Any]] = NOT_SET,
        response_schema: t.Any = NOT_SET,
        status_code: int = status.HTTP_200_OK,
        auth: t.Any = NOT_SET,
        throttle: t.Union[BaseThrottle, t.List[BaseThrottle], NOT_SET_TYPE] = NOT_SET,
        operation_id: t.Optional[str] = None,
        summary: t.Optional[str] = None,
        description: t.Optional[str] = None,
        tags: t.Optional[t.List[str]] = None,
        deprecated: t.Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        url_name: t.Optional[str] = None,
        include_in_schema: bool = True,
        permissions: t.Optional[
            t.List[t.Union[t.Type[BasePermission], BasePermission, t.Any]]
        ] = None,
        openapi_extra: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> t.Callable[[TCallable], TCallable]:
        """
        Internal shared decorator logic for all HTTP methods.

        Handles:
        - Wrapping response or response_schema into {status_code: schema}
        - Passing route parameters to the base Route class
        """
        if response_schema is not NOT_SET:
            response = {status_code: response_schema}
        elif response != NOT_SET and not isinstance(response, dict):
            response = {status_code: response}

        def decorator(view_func: TCallable) -> TCallable:
            return cls._create_route_function(
                view_func,
                path=path,
                methods=[method],
                auth=auth,
                response=response,
                operation_id=operation_id,
                summary=summary,
                description=description,
                tags=tags,
                deprecated=deprecated,
                by_alias=True,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                url_name=url_name,
                include_in_schema=include_in_schema,
                permissions=permissions,
                openapi_extra=openapi_extra,
                throttle=throttle,
            )
        return decorator

    @classmethod
    def get(cls, *args, **kwargs):
        """
        Shortcut for defining GET endpoints.

        Usage:
            @route.get("/path", response_schema=MySchema)
            def handler(...): ...
        """
        if args:
            kwargs["path"] = args[0]
        return cls._operation(GET, **kwargs)

    @classmethod
    def post(cls, *args, **kwargs):
        """
        Shortcut for defining POST endpoints.

        Usage:
            @route.post("/path", response_schema=MySchema)
            def handler(...): ...
        """
        if args:
            kwargs["path"] = args[0]
        return cls._operation(POST, **kwargs)

    @classmethod
    def put(cls, *args, **kwargs):
        """
        Shortcut for defining PUT endpoints.

        Usage:
            @route.put("/path", response_schema=MySchema)
            def handler(...): ...
        """
        if args:
            kwargs["path"] = args[0]
        return cls._operation(PUT, **kwargs)

    @classmethod
    def patch(cls, *args, **kwargs):
        """
        Shortcut for defining PATCH endpoints.

        Usage:
            @route.patch("/path", response_schema=MySchema)
            def handler(...): ...
        """
        if args:
            kwargs["path"] = args[0]
        return cls._operation(PATCH, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        """
        Shortcut for defining DELETE endpoints.

        Usage:
            @route.delete("/path", status_code=status.HTTP_204_NO_CONTENT, response_schema=MySchema)
            def handler(...): ...
        """
        if args:
            kwargs["path"] = args[0]
        return cls._operation(DELETE, **kwargs)


# Default import alias
route = AutoAliasRoute
