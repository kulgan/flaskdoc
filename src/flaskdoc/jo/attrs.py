""" Craft models using json schema

Example:
    .. code-block::

        from flaskdoc import jo

        @jo.schema()
        class Sample(object):
            age = jo.integer(required=True, minimum=18)
            name = jo.string(required=True)

"""
import attr

from flaskdoc.core import camel_case
from flaskdoc.swagger.schema import (
    Array,
    Boolean,
    Integer,
    Number,
    Object,
    Schema,
    String,
    schema_factory,
)

JO_SCHEMA = "__jo__"
JO_REQUIRED = "__jo__required__"


def schema(additional_properties=False, required=None, min_properties=None, max_properties=None):
    """ decorates a class automatically binding it to a Schema instance

    This technically extends `attr.s` amd pulls out a schema in the process

    Args:
        additional_properties (bool): True if additional properties are allowed
        required (bool): True if field is required
        min_properties (int):  Minimum number of properties allowed
        max_properties (int): Maximum number of properties allowed

    Returns:
        attr.s: and attr.s wrapped class
    """

    def wraps(cls):
        req = required or []
        setattr(cls, "additional_properties", additional_properties)

        def jo_schema(cls):
            sc = Object(
                additional_properties=additional_properties,
                required=req,
                min_properties=min_properties,
                max_properties=max_properties,
            )
            sc.properties = {}
            attributes = cls.__attrs_attrs__
            for attrib in attributes:
                psc = attrib.metadata[JO_SCHEMA]
                is_required = attrib.metadata.get(JO_REQUIRED, False)
                field_name = camel_case(attrib.name)
                if is_required and field_name not in sc.required:
                    sc.required.append(field_name)
                sc.properties[attrib.name] = psc
            return sc

        setattr(cls, "jo_schema", classmethod(jo_schema))
        return attr.s(cls)

    return wraps


def string(
    default=None,
    required=None,
    str_format=None,
    min_length=None,
    max_length=None,
    enum=None,
    example=None,
    description=None,
):
    sc = String(
        format=str_format,
        min_length=min_length,
        max_length=max_length,
        enum=enum,
        example=example,
        description=description,
    )
    return attr.ib(type=str, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def email(default=None, required=None, description=None):
    return string(default, str_format="email", required=required, description=description)


def number(
    default=None,
    minimum=None,
    maximum=None,
    int_format=None,
    multiple_of=None,
    exclusive_min=None,
    exclusive_max=None,
    required=None,
    read_only=None,
    write_only=None,
    example=None,
    description=None,
):
    sc = Number(
        format=int_format,
        minimum=minimum,
        maximum=maximum,
        example=example,
        read_only=read_only,
        write_only=write_only,
        multiple_of=multiple_of,
        exclusive_minimum=exclusive_min,
        exclusive_maximum=exclusive_max,
        description=description,
    )
    return attr.ib(type=float, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def integer(
    default=None,
    minimum=None,
    maximum=None,
    int_format=None,
    multiple_of=None,
    exclusive_min=None,
    exclusive_max=None,
    required=None,
    read_only=None,
    write_only=None,
    example=None,
    description=None,
):
    sc = Integer(
        format=int_format,
        minimum=minimum,
        maximum=maximum,
        example=example,
        description=description,
        read_only=read_only,
        write_only=write_only,
        multiple_of=multiple_of,
        exclusive_minimum=exclusive_min,
        exclusive_maximum=exclusive_max,
    )
    return attr.ib(type=float, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def one_of(types, default=None, discriminator=None, description=None):
    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(one_of=items, discriminator=discriminator, description=description)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def all_of(types, default=None, discriminator=None, description=None):
    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(all_of=items, discriminator=discriminator, description=description)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def any_of(types, default=None, discriminator=None):
    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(any_of=items, discriminator=discriminator)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def boolean(
    default=None, required=None, read_only=None, write_only=None, description=None,
):
    sc = Boolean(read_only=read_only, write_only=write_only, description=description)
    return attr.ib(type=bool, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def array(
    item=None, default=None, min_items=None, max_items=None, unique_items=None, required=None
):
    sc = Array(items=item, min_items=min_items, max_items=max_items, unique_items=unique_items)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def object(item, default=None, required=None, description=None):
    sc = schema_factory.get_schema(item, description=description)
    return attr.ib(type=item, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})
