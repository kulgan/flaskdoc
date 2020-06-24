from dataclasses import dataclass
import typing as t

from flaskdoc import swagger


@dataclass
class Boolean(swagger.Schema):
    type: str = "boolean"


@dataclass
class String(swagger.Schema):
    type: str = "string"


@dataclass
class Email(String):
    type: str = "string"
    format: str = "email"


@dataclass
class Int32(swagger.Schema):
    type: str = "integer"
    format: str = "int32"
    minimum: int = 0


@dataclass
class Number(Int32):
    type: str = "number"


@dataclass
class Int64(Int32):
    format: str = "int64"


@dataclass
class Base64String(String):
    format: str = "base64"


@dataclass
class BinaryString(String):
    format: str = "binary"


@dataclass
class Image(BinaryString):
    pass


class MultipartFormData:
    pass


@dataclass
class Array(swagger.Schema):
    type: str = "array"


_MAP = {
    str: String,
    int: Int32,
    bool: Boolean,
    float: Number,
    t.Text: String,
    t.AnyStr: String,
    t.ByteString: BinaryString,
}


class TypesFactory:
    @classmethod
    def get(cls, _type: t.Type, **kwargs):
        schema_class = _MAP.get(_type)
        if schema_class:
            return schema_class(**kwargs)
        raise ValueError("Unsupported object type: {}".format(_type))


class SchemaFactory:
    def __init__(
        self, ref_base: str = "#/definitions", schema_key: str = "definitions"
    ):
        self.ref_base = ref_base
        self.schema_key = schema_key
        self.schema = {schema_key: {}}

    def from_type(self, _type: t.Type):
        # is typing Alias?
        if not isinstance(_type, type):
            pass
