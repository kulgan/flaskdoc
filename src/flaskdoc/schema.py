""" Provides implementations of JSON schema objects and a factory instance

    The Schema class conforms to openapi schema definition, also provides ready
    to use implementations for String, Number, Boolean etc, these objects can readily
    be converted to json schemas

    Examples:
        >> string = String(description="spoils")
        >> string.type
        spoils
        >> string.to_dict()
        {"type": "string", "description": "spoils"}

    Also provides fully implemented mume types
"""
import collections
import inspect
from collections import defaultdict
from typing import AnyStr, ByteString, Dict, List, Set, Text, Union

import attr

from flaskdoc.core import ModelMixin


@attr.s
class Content(object):
    """ A content container for response and request objects """

    content_type = attr.ib(type=str)
    schema = attr.ib(type=type)
    description = attr.ib(default=None, type=str)

    def to_schema(self):

        # handle primitives
        if self.schema in [str, int, bool, dict]:
            schema_class = SCHEMA_TYPES_MAP[self.schema]
            schema = schema_class()
            schema.description = self.description or schema.description
            return schema
        # handle schema derivatives
        if isinstance(self.schema, Schema):
            self.schema.description = self.description or self.schema.description
            return self.schema
        # handle custom class types
        return schema_factory.get_schema(self.schema)


@attr.s
class JsonType(Content):
    """ mime type application/json content type """

    content_type = attr.ib(default="application/json", init=False)


@attr.s
class PlainText(Content):
    content_type = attr.ib(default="text/plain", init=False)


@attr.s
class Schema(ModelMixin):
    """ The Schema Object allows the definition of input and output data types.

    These types can be objects, but also primitives and arrays. This object is an extended subset of the JSON Schema
    Specification Wright Draft 00. For more information about the properties, see JSON Schema Core and JSON Schema
    Validation. Unless stated otherwise, the property definitions follow the JSON Schema.
    """

    ref = attr.ib(default=None, type=str)
    title = attr.ib(default=None, type=str)
    multiple_of = None
    maximum = attr.ib(default=None, type=int)
    exclusive_maximum = None
    minimum = None
    exclusive_minimum = None
    max_length = None  # type: int
    min_length = None  # type: int
    pattern = None
    max_items = None  # type: ignore
    min_items = None  # type: ignore
    unique_item = None
    max_properties = None  # type: ignore
    min_properties = None  # type: ignore
    required = None
    enum = None
    type = attr.ib(default=None, type=str)
    all_of = None
    one_of = None
    any_of = None
    _not = None  # type: ignore
    items = attr.ib(default=None)
    properties = attr.ib(default=None, type=dict, init=False)
    additional_properties = None
    description = attr.ib(default=None, type=str)
    format = attr.ib(default=None, type=str)
    default = None
    nullable = None
    discriminator = None
    read_only = None
    write_only = None
    xml = None
    external_docs = None
    example = None
    deprecated = None

    def q_not(self):
        return self._not

    def __attrs_post_init__(self):
        # register schema
        if self.items:
            self.items = schema_factory.get_schema(self.items)


@attr.s
class Boolean(Schema):
    type = attr.ib(default="boolean", init=False)


@attr.s
class String(Schema):
    type = attr.ib(default="string", init=False)


@attr.s
class Email(String):
    type = attr.ib(default="string", init=False)
    format = attr.ib(default="email", init=False)


@attr.s
class Int32(Schema):
    type = attr.ib(default="integer", init=False)
    format = attr.ib(default="int32", init=False)
    minimum = attr.ib(default=0, type=int)


@attr.s
class Number(Int32):
    type = attr.ib(default="number", init=False)
    format = attr.ib(default=None, init=False)


@attr.s
class Int64(Int32):
    format = attr.ib(default="int64", init=False)


@attr.s
class Base64String(String):
    format = attr.ib(default="base64", init=False)


@attr.s
class BinaryString(String):
    format = attr.ib(default="binary", init=False)


@attr.s
class Image(BinaryString):
    pass


class MultipartFormData:
    pass


@attr.s
class Object(Schema):
    type = attr.ib(default="object", init=False)


@attr.s
class Array(Schema):
    items = attr.ib(default=None)
    type = attr.ib(default="array", init=False)

    @items.validator
    def validate(self, _, items):
        if not items:
            raise ValueError("items must be specified for Array schema")


@attr.s
class ContentMixin(object):

    content = attr.ib()  # type: Union[Content, List[Content]]

    def __attrs_post_init__(self):

        if not self.content:
            return

        if not isinstance(self.content, list):
            self.content = [self.content]
        cnt = defaultdict(dict)
        for content in self.content:
            cnt[content.content_type]["schema"] = content.to_schema()
        self.content = cnt


@attr.s
class SchemaFactory(object):

    ref_base = attr.ib(default="#/components/schemas", init=False)
    components = attr.ib(init=False, default={})
    class_map = attr.ib(init=False, default={})

    def parse_data_fields(self, cls, fields):
        """ Parses classes implemented using either py37 dataclasses or attrs

        Args:
            cls (class):
            fields (dict):

        Returns:

        """
        if isinstance(fields, dict):
            fields = fields.values()
        for props in fields:
            field_type = props.type or type(props.default) if props.default else str
            self.class_map[cls.__name__][props.name] = self.get_schema(field_type)

    def from_type(self, cls):

        if cls.__name__ in self.class_map:
            return self.class_map[cls.__name__]

        self.class_map[cls.__name__] = {}
        annotations = cls.__annotations__ if hasattr(cls, "__annotations__") else {}
        members = inspect.getmembers(cls)
        for field, member in members:

            if field in ["__dataclass_fields__", "__attrs_attrs__"]:
                self.parse_data_fields(cls, member)
                continue

            # skip private members and methods
            if not (
                field.startswith("_") or inspect.ismethod(member) or inspect.isfunction(member)
            ):
                field_type = type(member) if member else annotations.get(field)
                field_type = field_type or str
                self.class_map[cls.__name__][field] = self.get_schema(field_type)

        return self.class_map[cls.__name__]

    def get_schema(self, cls, description=None):
        # handle schema derivatives
        if isinstance(cls, Schema):
            cls.description = description or cls.description
            return cls
        # if raw dict instances
        if isinstance(cls, collections.Mapping):
            schema = Object(description=description)
            properties = {}
            for k, v in cls.items():
                properties[k] = self.get_schema(v)
            schema.properties = properties
            return schema

        # if raw list
        if isinstance(cls, (set, list)):
            return Array(items=self.get_schema(cls[0], description=description))

        # handle primitives
        if cls in SCHEMA_TYPES_MAP:
            schema_class = SCHEMA_TYPES_MAP[cls]
            return schema_class()
        # collection based typing
        if hasattr(cls, "__origin__"):
            origin = cls.__origin__
            if origin in [list, set, List, Set]:
                args = cls.__args__[0]
                arg_schema = self.get_schema(args)
                return Array(items=arg_schema, description=description)
            if origin in [dict, Dict]:
                pass

        sch = Object()
        sch.properties = self.from_type(cls)
        self.components[cls.__name__] = sch
        return Schema(
            ref="{}/{}".format(self.ref_base, cls.__name__), description=inspect.getdoc(cls)
        )


SCHEMA_TYPES_MAP = {
    int: Int32,
    str: String,
    bool: Boolean,
    dict: Object,
    list: Array,
    float: Number,
    Text: String,
    AnyStr: String,
    ByteString: BinaryString,
}
schema_factory = SchemaFactory()
