"""" OpenAPI specific Json Schema Objects implementation and factory

    The Schema class conforms to openapi schema definition, also provides ready
    to use implementations for String, Number, Boolean etc, these objects can readily
    be converted to json schemas

    Examples:
        >>> string = String(description="spoils")
        >>> string.description
        spoils
        >>> string.to_dict()
        {"type": "string", "description": "spoils"}

    Also provides some common mime types like JsonType, XmlType
"""
import collections
import enum
import inspect
from collections import defaultdict
from typing import AnyStr, ByteString, Dict, List, Set, Text, Union

import attr

from flaskdoc.core import ExtensionMixin, ModelMixin


@attr.s
class Schema(ModelMixin):
    """The Schema Object allows the definition of input and output data types.

    These types can be objects, but also primitives and arrays. This object is an extended subset of the JSON Schema
    Specification Wright Draft 00. For more information about the properties, see JSON Schema Core and JSON Schema
    Validation. Unless stated otherwise, the property definitions follow the JSON Schema.
    """

    ref = attr.ib(default=None, type=str)
    title = attr.ib(default=None, type=str)
    multiple_of = attr.ib(default=None, type=float)
    maximum = attr.ib(default=None, type=int)
    minimum = attr.ib(default=None, type=int)
    exclusive_maximum = attr.ib(default=None, type=bool)
    exclusive_minimum = attr.ib(default=None, type=bool)
    max_length = attr.ib(default=None, type=int)  # type: int
    min_length = attr.ib(default=None, type=int)  # type: int
    pattern = attr.ib(default=None, type=str)
    max_items = attr.ib(default=None, type=int)  # type: ignore
    min_items = attr.ib(default=None, type=int)  # type: ignore
    unique_items = attr.ib(default=None, type=bool)
    max_properties = attr.ib(default=None, type=int)  # type: ignore
    min_properties = attr.ib(default=None, type=int)  # type: ignore
    enum = attr.ib(default=None, type=List)
    type = attr.ib(default=None, type=str)
    all_of = attr.ib(default=None, type=List["Schema"])
    one_of = attr.ib(default=None, type=List["Schema"])
    any_of = attr.ib(default=None, type=List["Schema"])
    _not = None  # type: ignore
    items = attr.ib(default=None)
    properties = attr.ib(default=None, type=dict)
    additional_properties = attr.ib(type=bool, default=None)
    description = attr.ib(default=None, type=str)
    format = attr.ib(default=None, type=str)
    default = attr.ib(default=None)
    nullable = attr.ib(default=None, type=bool)
    discriminator = attr.ib(default=None, type="Discriminator")
    read_only = attr.ib(default=None, type=bool)
    write_only = attr.ib(default=None, type=bool)
    xml = attr.ib(default=None, type="XML")
    external_docs = None
    deprecated = attr.ib(default=None, type=bool)
    example = attr.ib(default=None, type=dict)

    def q_not(self):
        return self._not

    def __attrs_post_init__(self):
        # register schema
        if self.items:
            self.items = schema_factory.get_schema(self.items)
        if isinstance(self.xml, str):
            self.xml = XML(name=self.xml)

        # resolve properties
        self._resolve_properties()

    def _resolve_properties(self):
        if self.properties:
            props = {}
            for k, v in self.properties.items():
                if not isinstance(v, Schema):
                    props[k] = schema_factory.get_schema(v)
                else:
                    props[k] = v
            self.properties = props


@attr.s
class Boolean(Schema):
    example = attr.ib(default=None, type=bool)
    type = attr.ib(default="boolean", init=False)


@attr.s
class String(Schema):
    example = attr.ib(default=None, type=str)
    type = attr.ib(default="string", init=False)


@attr.s
class Email(String):
    type = attr.ib(default="string", init=False)
    format = attr.ib(default="email", init=False)


@attr.s
class Number(Schema):
    example = attr.ib(default=None, type=float)
    type = attr.ib(default="number", init=False)


@attr.s
class Integer(Number):
    type = attr.ib(default="integer", init=False)
    format = attr.ib(default="int32", type=str)
    example = attr.ib(default=None, type=int)


@attr.s
class Base64String(String):
    format = attr.ib(default="base64", init=False)


@attr.s
class BinaryString(String):
    format = attr.ib(default="binary", init=False)


@attr.s
class Object(Schema):
    type = attr.ib(default="object", init=False)
    required = attr.ib(default=None, type=list)


@attr.s
class XML(ModelMixin):
    """A metadata object that allows for more fine-tuned XML model definitions. When using arrays, XML element names
    are not inferred (for singular/plural forms) and the name property SHOULD be used to add that information. See
    examples for expected behavior.
    """

    name = attr.ib(default=None, type=str)
    namespace = attr.ib(default=None, type=str)
    prefix = attr.ib(default=None, type=str)
    attribute = attr.ib(default=None, type=bool)
    wrapped = attr.ib(default=None, type=bool)


@attr.s
class Discriminator(ModelMixin):
    """When request bodies or response payloads may be one of a number of different schemas, a discriminator object
    can be used to aid in serialization, deserialization, and validation. The discriminator is a specific object in a
    schema which is used to inform the consumer of the specification of an alternative schema based on the value
    associated with it."""

    property_name = attr.ib(type=str)
    mapping = attr.ib(default=dict)


@attr.s
class Int64(Integer):
    format = attr.ib(default="int64", init=False)


@attr.s
class Image(BinaryString):
    pass


@attr.s
class Array(Schema):
    items = attr.ib(default=None)
    type = attr.ib(default="array", init=False)

    @items.validator
    def validate(self, _, items):
        if not items:
            raise ValueError("items must be specified for Array schema")


@attr.s
class SchemaFactory(object):
    """Converts an object into a json schema and returns a reference

    Properties:
        ref_base (str): json schema reference base, defaults to `#/components/schema`
        components (dict[class, dict]): class and schema representation
    """

    ref_base = attr.ib(default="#/components/schemas")
    schemas = attr.ib(init=False, default={})
    examples = attr.ib(init=False, default={})

    def parse_data_fields(self, cls, fields):
        """Parses classes implemented using either py37 dataclasses or attrs

        Args:
            cls (class):
            fields (dict):

        Returns:

        """
        if isinstance(fields, dict):
            fields = fields.values()
        for props in fields:
            field_type = props.type or type(props.default) if props.default else str
            CLASS_MAP[cls.__name__][props.name] = self.get_schema(field_type)

    def from_type(self, cls):

        if cls.__name__ in CLASS_MAP:
            return CLASS_MAP[cls.__name__]

        CLASS_MAP[cls.__name__] = {}
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
                CLASS_MAP[cls.__name__][field] = self.get_schema(field_type)

        return CLASS_MAP[cls.__name__]

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
                return Object(additional_properties=True, description=description)

        if isinstance(cls, enum.EnumMeta):
            enums = []
            sch_type = Schema
            for c in cls.__members__.values():
                v = c._value_
                enums.append(v)
                if v:
                    sch_type = SCHEMA_TYPES_MAP.get(type(v))
            sch = sch_type(enum=enums, description=description)
        # handle custom jo objects
        elif hasattr(cls, "jo_schema"):
            sch = cls.jo_schema()
        else:
            sch = Object()
            sch.properties = self.from_type(cls)
        self.schemas[cls.__name__] = sch
        return Schema(ref="{}/{}".format(self.ref_base, cls.__name__))

    def clear(self):
        self.schemas = {}


@attr.s
class MediaType(ModelMixin):
    """Each Media Type Object provides schema and examples for the media type identified by its key."""

    content_type = attr.ib(type=str)
    schema = attr.ib(default=None, type="Schema")
    example = attr.ib(default=None)
    examples = attr.ib(default=None, type=dict)

    def to_schema(self):

        if not self.schema:
            return None

        # handle primitives
        if self.schema in [str, int, bool, dict]:
            schema_class = SCHEMA_TYPES_MAP[self.schema]
            schema = schema_class()
            return schema
        # handle schema derivatives
        if isinstance(self.schema, Schema):
            return self.schema
        # handle custom class types
        return schema_factory.get_schema(self.schema)

    def to_dict(self):
        return dict(
            schema=self.to_schema(),
            example=self.example,
            examples=self.examples,
        )


@attr.s
class JsonType(MediaType):
    """mime type application/json content type"""

    content_type = attr.ib(default="application/json", init=False)


@attr.s
class PlainText(MediaType):
    content_type = attr.ib(default="text/plain", init=False)


@attr.s
class UrlEncodedFormType(MediaType):
    content_type = attr.ib(default="application/x-www-form-urlencoded", init=False)
    encoding = attr.ib(default=None, type=Dict[str, "Encoding"])

    def to_dict(self):
        d = super(UrlEncodedFormType, self).to_dict()
        d["encoding"] = self.encoding
        return d


@attr.s
class MultipartType(UrlEncodedFormType):

    content_type = attr.ib(default="multipart/form-data")

    @content_type.validator
    def validate(self, attribute, ctype):
        if not ctype.startswith("multipart"):
            raise ValueError(
                "Attribue {} value must start with multipart and not {}".format(
                    attribute, self.content_type
                )
            )


@attr.s
class XmlType(MediaType):
    content_type = attr.ib(default="application/xml", init=False)


@attr.s
class MultipartFormData:
    file = BinaryString()


SCHEMA_TYPES_MAP = {
    int: Integer,
    str: String,
    bool: Boolean,
    dict: Object,
    list: Array,
    float: Number,
    Text: String,
    AnyStr: String,
    ByteString: BinaryString,
}
CLASS_MAP = {}
schema_factory = SchemaFactory()


@attr.s
class ContentMixin(object):

    content = attr.ib()  # type: Union[MediaType, List[MediaType]]

    def __attrs_post_init__(self):

        if not self.content:
            return

        if not isinstance(self.content, list):
            self.content = [self.content]
        cnt = defaultdict(dict)
        for content in self.content:
            cnt[content.content_type] = content.to_dict()
        self.content = cnt


@attr.s
class Encoding(ExtensionMixin):
    """A single encoding definition applied to a single schema property."""

    content_type = attr.ib(type=str)
    headers = attr.ib(default=None, type=dict)
    style = attr.ib(default=None, type="Style")
    explode = attr.ib(default=True)
    allow_reserved = attr.ib(default=False)
    extensions = attr.ib(default={})

    def add_header(self, name, header):
        if not self.headers:
            self.headers = {}
        self.headers[name] = header


@attr.s
class Example(ExtensionMixin):

    summary = attr.ib(default=None, type=str)
    description = attr.ib(default=None, type=str)
    value = attr.ib(default=None)
    external_value = attr.ib(default=None, type=str)
    extensions = attr.ib(default={})
