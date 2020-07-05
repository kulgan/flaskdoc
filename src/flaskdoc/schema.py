import typing as t

import attr

from flaskdoc import swagger


@attr.s
class Boolean(swagger.Schema):
    type = attr.ib(default="boolean", init=False)


@attr.s
class String(swagger.Schema):
    type = attr.ib(default="string", init=False)


@attr.s
class Email(String):
    type = attr.ib(default="string", init=False)
    format = attr.ib(default="email", init=False)


@attr.s
class Int32(swagger.Schema):
    type = attr.ib(default="integer", init=False)
    format = attr.ib(default="int32", init=False)
    minimum = attr.ib(default=0, type=int)


@attr.s
class Number(Int32):
    type = attr.ib(default="number", init=False)


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
class Object(swagger.Schema):
    type = attr.ib(default="object", init=False)

    @classmethod
    def from_class(cls, class_type):
        return cls()


@attr.s
class Array(swagger.Schema):
    type = attr.ib(default="array", init=False)


@attr.s
class Content(object):
    item = attr.ib(type=type)
    is_array = attr.ib(default=False)
    type = attr.ib(default="application/json", type=str)

    def __attrs_post_init__(self):
        pass


@attr.s
class JsonContent(Content):
    type = attr.ib(init=False, default="application/json")


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
    def __init__(self, ref_base: str = "#/definitions", schema_key: str = "definitions"):
        self.ref_base = ref_base
        self.schema_key = schema_key
        self.schema = {schema_key: {}}

    def from_type(self, _type: t.Type):
        # is typing Alias?
        if not isinstance(_type, type):
            pass


if __name__ == "__main__":
    print(isinstance(String, swagger.Schema))
