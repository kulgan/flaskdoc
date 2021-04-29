""" Craft models using json schema


"""
import attr

from flaskdoc.core import camel_case
from flaskdoc.swagger import (
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


def schema(
    additional_properties=None,
    required=None,
    min_properties=None,
    max_properties=None,
    xml=None,
    camel_case_props=False,
):
    """decorates a class automatically binding it to a Schema instance

    This technically extends `attr.s` amd pulls out a Schema instance in the process

    Args:
        additional_properties (bool): True if additional properties are allowed
        required (list[str]): list of required property names
        min_properties (int):  Minimum number of properties allowed
        max_properties (int): Maximum number of properties allowed
        xml (str|flaskdoc.swagger.XML): swagger XML object instance or string representing the name of the XML field
        camel_case_props (bool): If True model properties are converted to camel case
    Returns:
        attr.s: and attr.s wrapped class

    Example:
        .. code-block::

            from flaskdoc import jo

            @jo.schema(xml="Sample")
            class Sample(object):
                age = jo.integer(required=True, minimum=18)
                name = jo.string(required=True)

    """

    def wraps(cls):
        req = required or []
        setattr(cls, "additional_properties", additional_properties)

        def jo_schema(cls):
            sc = Object(
                additional_properties=additional_properties,
                min_properties=min_properties,
                max_properties=max_properties,
                xml=xml,
            )
            sc.properties = {}
            attributes = cls.__attrs_attrs__
            for attrib in attributes:
                psc = attrib.metadata[JO_SCHEMA]
                is_required = attrib.metadata.get(JO_REQUIRED, False)
                field_name = camel_case(attrib.name) if camel_case_props else attrib.name
                if is_required and field_name not in req:
                    req.append(field_name)
                sc.properties[field_name] = psc

            if req:
                sc.required = req
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
    xml=None,
):
    """Creates a json schema of type string

    Args:
        default (str): default value
        required (bool): True if it should be required in the schema
        str_format (str): string format, can be uuid, email, binary etc
        min_length (int): minimum length of the string
        max_length (int): maximum length of the strin
        enum (enum.Enum): represent schema as an enum instead of free text
        example (str): Examole string
        description (str): Property description
        xml (str|flaskdoc.swagger.XML): xml name of XML object instance

    Returns:
        attr.ib: field definition
    """
    sc = String(
        format=str_format,
        min_length=min_length,
        max_length=max_length,
        enum=enum,
        example=example,
        description=description,
        xml=xml,
    )
    return attr.ib(type=str, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def email(default=None, required=None, description=None, xml=None):
    return string(
        default, str_format="email", required=required, description=description, xml=xml
    )


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
    xml=None,
):
    """Create a schema of type number"""

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
        xml=xml,
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
    xml=None,
):
    """Create a schema of type integer"""

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
        xml=xml,
    )
    return attr.ib(type=float, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def one_of(types, default=None, discriminator=None, description=None):
    """Applies to properties and complies with JSON schema oneOf property

    Args:
        types (list[type]): list of types that will be allowed
        default (object): default object instance that must be one of the allowed types
        discriminator:
        description (str): summary of property

    Returns:
        attr.ib: field instance
    """
    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(one_of=items, discriminator=discriminator, description=description)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def all_of(types, default=None, discriminator=None, description=None):
    """JSON schema allOf"""

    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(all_of=items, discriminator=discriminator, description=description)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def any_of(types, default=None, discriminator=None):
    """JSON schema anyOf"""

    items = [schema_factory.get_schema(cls) for cls in types]
    sc = Schema(any_of=items, discriminator=discriminator)
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc})


def boolean(
    default=None,
    required=None,
    read_only=None,
    write_only=None,
    description=None,
    xml=None,
):
    """Boolean schema data type

    Args:
        default:
        required (bool):
        read_only (bool):
        write_only (bool):
        description (str): summary/description
        xml: XML name or XML object instance

    Returns:
        attr.ib:
    """
    sc = Boolean(read_only=read_only, write_only=write_only, description=description, xml=xml)
    return attr.ib(type=bool, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def array(
    item=None,
    default=None,
    min_items=None,
    max_items=None,
    unique_items=None,
    required=None,
    xml=None,
):
    """Array data type"""
    sc = Array(
        items=item, min_items=min_items, max_items=max_items, unique_items=unique_items, xml=xml
    )
    return attr.ib(type=list, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})


def object(item, default=None, required=None, description=None):
    """Raw object data type"""

    sc = schema_factory.get_schema(item, description=description)
    return attr.ib(type=item, default=default, metadata={JO_SCHEMA: sc, JO_REQUIRED: required})
