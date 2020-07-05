import inspect
import typing as t

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


class SchemaFactory:
    def __init__(self, ref_base: str = "#/definitions", schema_key: str = "definitions"):
        self.ref_base = ref_base
        self.schema_key = schema_key
        self.schema = {schema_key: {}}

    def generate_schema(self, obj: t.Type):

        if isinstance(obj, type):
            _type = schema_types_map.get_type(obj)
        elif hasattr(obj, "__origin__"):
            _type = schema_types_map.get_type(obj.__origin__)
        # base case
        if schema_types_map.is_simple_type(_type):
            return self._generate_simple(_type)

        if schema_types_map.is_array_type(_type):
            pass

        return self._generate_object(obj)

    def _generate_simple(self, type_name: str):
        return dict(type=type_name)

    def _generate_array(self, obj_type: t.Union[t.List, t.Set]):
        return dict(type="array")

    def _generate_object(self, obj_type: t.Type):

        props = {}
        properties = et(obj_type)
        for prop, _type in properties.items():
            props[prop] = self.generate_schema(_type)
        schema = dict(type="object", properties=props)
        self.schema[self.schema_key][obj_type.__name__] = schema
        return {"$ref": "{}/{}".format(self.ref_base, obj_type.__name__)}


@attr.s
class Soap(object):

    meal = attr.ib(type=float)
    smokes = attr.ib(type=list)


@attr.s
class Sample(object):

    palo = attr.ib(type=int)
    soap = attr.ib(type=Soap)
    hulu = attr.ib(default="NoNo")


CLASS_MAP = {}


def et(cls):

    if cls.__name__ in CLASS_MAP:
        return CLASS_MAP[cls.__name__]

    CLASS_MAP[cls.__name__] = {}
    members = inspect.getmembers(cls)
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

    print(et(Sample))
