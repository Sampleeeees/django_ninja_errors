"""
Base django schema.
"""

import json
from typing import Any

from humps.main import camelize
from ninja import Schema


class DjangoSchema(Schema):
    """
    Base schema for all API schemas.
    """

    class Config(Schema.Config):
        """
        Pydantic config.
        """

        from_attributes = True
        alias_generator = camelize
        populate_by_name = True
        str_strip_whitespace = True

    def compute(self):
        """Compute all fields."""
        pass

    def adjust(self, **kwargs):
        """Adjust fields."""
        if isinstance(super(), DjangoSchema):
            super().adjust(**kwargs)  # noqa

        # call adjust method for all attributes that have it
        for attr in self.__dict__.values():
            if isinstance(attr, DjangoSchema):
                attr.adjust(**kwargs)

        return self

    @classmethod
    def from_orm(cls, obj: Any):
        """Create schema from ORM model."""
        obj = super().from_orm(obj)
        obj.compute()  # noqa
        return obj

    @classmethod
    def from_orm_adjusted(cls, obj: Any, **kwargs):
        """Create schema from ORM model."""
        obj = super().from_orm(obj)
        obj.adjust(**kwargs)  # noqa
        return obj

    @classmethod
    def from_list(cls, objs: list[Any]):
        """Create schema from ORM model."""
        objs = [cls.from_orm(obj) for obj in objs]
        return objs

    @classmethod
    def from_list_adjusted(cls, objs: list[Any], **kwargs):
        """Adjust list of objects."""
        objs = cls.from_list(objs)
        [obj.adjust(**kwargs) for obj in objs]
        return objs

    @classmethod
    def async_schema(cls, **kwargs):
        """
        Return async schema.
        """
        schema = cls.schema()
        schema.pop("definitions", None)
        schema_str = json.dumps(schema)
        schema_str = schema_str.replace("#/definitions/", "#/components/schemas/")
        return json.loads(schema_str)
