"""
Custom django ninja Route class.
"""
from ninja_extra.controllers import Route


class AutoAliasRoute(Route):
    """Route with by_alias=True for Pydantic models."""

    def __init__(self, *args, **kwargs):
        """Initialize route."""
        super().__init__(*args, **kwargs)

        # set by_alias always True
        self.route_params.by_alias = True


route = AutoAliasRoute