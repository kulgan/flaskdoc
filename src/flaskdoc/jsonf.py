import inspect
import typing as t
from dataclasses import dataclass

import attr


class SchemaTypeMap:
    TYPES_MAP = {
        str: "string",
        int: "integer",
        bool: "boolean",
        dict: "object",
        set: "array",
        list: "array",
        float: "number",
        None: "null",
    }

    SIMPLE_TYPES = [
        "string",
        "number",
        "integer",
        "boolean",
    ]

    def get_type(self, _type: t.Type):
        return self.TYPES_MAP.get(_type)

    def is_simple_type(self, type_name: str):
        return type_name in self.SIMPLE_TYPES

    def is_array_type(self, type_name: str):
        return type_name == "array"


schema_types_map = SchemaTypeMap()


@attr.s
class SchemaFactory:

    ref_base = attr.ib(default="#/definitions", type=str)
    schema_key = attr.ib(default="definitions", type=str)
    schema = attr.ib(init=False, default={})
    class_map = attr.ib(init=False, default={})

    def __attrs_post_init__(self):
        self.schema = {self.schema_key: {}}

    def generate_schema(self, cls: t.Type):

        if isinstance(cls, type):
            _type = schema_types_map.get_type(cls)
        elif hasattr(cls, "__origin__"):
            _type = schema_types_map.get_type(cls.__origin__)
        else:
            _type = cls
        # base case
        if schema_types_map.is_simple_type(_type):
            return self._generate_simple(_type)

        if schema_types_map.is_array_type(_type):
            return ""

        return self._generate_object(cls)

    def _generate_simple(self, type_name: str):
        return dict(type=type_name)

    def _generate_array(self, obj_type: t.Union[t.List, t.Set]):
        return dict(type="array")

    def _generate_object(self, obj_type: t.Type):

        props = {}
        properties = self.from_type(obj_type)
        for prop, _type in properties.items():
            props[prop] = self.generate_schema(_type)
        schema = dict(type="object", properties=props)
        self.schema[self.schema_key][obj_type.__name__] = schema
        return {"$ref": "{}/{}".format(self.ref_base, obj_type.__name__)}

    def from_type(self, cls):

        if cls.__name__ in self.class_map:
            return self.class_map[cls.__name__]

        self.class_map[cls.__name__] = {}
        annotations = cls.__annotations__ if hasattr(cls, "__annotations__") else {}
        members = inspect.getmembers(cls)
        for field, member in members:

            if field == "__dataclass_fields__":
                self._parse_dataclass_fields(cls, member)
                continue
            if field == "__attrs_attrs__":
                self._parse_attrs_fields(cls, member)
                continue

            # skip private members and methods
            if not (field.startswith("_") or inspect.ismethod(member) or inspect.isfunction(member)):
                field_type = type(member) if member else annotations.get(field)
                field_type = field_type or str
                self.class_map[cls.__name__][field] = field_type

        return self.class_map[cls.__name__]

    def _parse_dataclass_fields(self, cls, fields):
        """

        Args:
            cls (class):
            fields (dict):

        Returns:

        """
        for _, props in fields.items():
            self.class_map[cls.__name__][props.name] = props.type

    def _parse_attrs_fields(self, cls, fields):
        """

        Args:
            cls (class):
            fields (dict):

        Returns:

        """
        for props in fields:
            field_type = props.type or type(props.default) if props.default else str
            self.class_map[cls.__name__][props.name] = field_type


@attr.s
class Soap(object):

    meal = attr.ib(type=float)
    smokes = attr.ib(default=10)


@attr.s
class Sample(object):
    danni = "fear"
    palo = attr.ib(type=int)
    soap = attr.ib(type=Soap)
    hulu = attr.ib(default="NoNo")


class OakTown:
    oaks = None
    smugs: int = 0
    snux = "2"


@dataclass
class Squeezed:

    sample: int
    spaces: str

    def hangout(self):
        return self.sample


CLASS_MAP = {}


def et(cls):

    if cls.__name__ in CLASS_MAP:
        return CLASS_MAP[cls.__name__]

    CLASS_MAP[cls.__name__] = {}
    members = inspect.getmembers(cls)
    if hasattr(cls, "__annotations__"):
        for field, _type in cls.__annotations__.items():
            CLASS_MAP[cls.__name__][field] = _type
    for field, val in members:
        if field.startswith("_") or inspect.ismethod(field):
            continue
        CLASS_MAP[cls.__name__][field] = type(val)

    return CLASS_MAP[cls.__name__]


if __name__ == "__main__":
    f = SchemaFactory()
    f.generate_schema(Sample)
    print(f.schema)
