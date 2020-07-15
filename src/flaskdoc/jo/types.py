import attr

from flaskdoc.jo.schema import (
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
                if is_required:
                    sc.required.append(attrib.name)
                sc.properties[attrib.name] = psc
            return sc

        setattr(cls, "jo_schema", classmethod(jo_schema))
        return attr.s(cls)

    return wraps


def string(
    default=None,
    required=None,
    format=None,
    min_length=None,
    max_length=None,
    enum=None,
    example=None,
):
    sc = String(
        format=format, min_length=min_length, max_length=max_length, enum=enum, example=example
    )
    return attr.ib(type=str, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def email(default=None, required=None):
    return string(default, format="email", required=required)


def number(
    default=None,
    minimum=None,
    maximum=None,
    format=None,
    multiple_of=None,
    exclusive_min=None,
    exclusive_max=None,
    required=None,
    read_only=None,
    write_only=None,
    example=None,
):
    sc = Number(
        format=format,
        minimum=minimum,
        maximum=maximum,
        example=example,
        read_only=read_only,
        write_only=write_only,
        multiple_of=multiple_of,
        exclusive_minimum=exclusive_min,
        exclusive_maximum=exclusive_max,
    )
    return attr.ib(type=float, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def integer(
    default=None,
    minimum=None,
    maximum=None,
    format=None,
    multiple_of=None,
    exclusive_min=None,
    exclusive_max=None,
    required=None,
    read_only=None,
    write_only=None,
    example=None,
):
    sc = Integer(
        format=format,
        minimum=minimum,
        maximum=maximum,
        example=None,
        read_only=read_only,
        write_only=write_only,
        multiple_of=multiple_of,
        exclusive_minimum=exclusive_min,
        exclusive_maximum=exclusive_max,
    )
    return attr.ib(type=float, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def one_of(types, default=None, discriminator=None):
    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(one_of=items, discriminator=discriminator)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def all_of(types, default=None, discriminator=None):
    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(all_of=items, discriminator=discriminator)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def any_of(types, default=None, discriminator=None):
    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(any_of=items, discriminator=discriminator)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def boolean(
    default=None, required=None, read_only=None, write_only=None,
):
    sc = Boolean(read_only=read_only, write_only=write_only)
    return attr.ib(type=bool, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def array(
    item=None, default=None, min_items=None, max_items=None, unique_items=None, required=None
):
    sc = Array(items=item, min_items=min_items, max_items=max_items, unique_items=unique_items)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def object(item, default=None, required=None):
    sc = schema_factory.get_schema(item)
    return attr.ib(type=item, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})
