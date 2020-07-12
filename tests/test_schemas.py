import sys
import typing as t

import pytest

from flaskdoc.schema import SchemaFactory
from tests.schema import models


@pytest.fixture()
def schema_factory():
    return SchemaFactory()


def test_to_schema(schema_factory):
    schema = schema_factory.get_schema(models.OakTown)
    assert schema.ref == "#/components/schemas/OakTown"


@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_to_schema_py36(schema_factory):
    from tests.schema.py36models import SoakedBean

    schema = schema_factory.get_schema(SoakedBean)
    assert schema.ref == "#/components/schemas/SoakedBean"


@pytest.mark.parametrize(
    "cls, exp, form",
    [
        (str, "string", None),
        (int, "integer", "int32"),
        (bool, "boolean", None),
        (float, "number", None),
        (t.Text, "string", None),
        (t.AnyStr, "string", None),
        (t.ByteString, "string", "binary"),
    ],
)
def test_primitives_to_schema(schema_factory, cls, exp, form):
    schema = schema_factory.get_schema(cls)
    assert schema.type == exp
    assert schema.format == form


@pytest.mark.parametrize(
    "cls, exp",
    [
        (str, dict(type="string")),
        (int, dict(type="integer", format="int32", minimum=0)),
        (bool, dict(type="boolean")),
        (float, dict(type="number", minimum=0)),
        (t.ByteString, dict(type="string", format="binary")),
        (dict, dict(type="object")),
        (t.List[str], dict(type="array", items=dict(type="string"))),
        (
            [models.OakTown],
            dict(
                type="array",
                items={
                    "$ref": "#/components/schemas/OakTown",
                    "description": "Sample class without any special annotations ",
                },
            ),
        ),
        (
            {"town": models.OakTown},
            dict(
                type="object",
                properties=dict(
                    town={
                        "$ref": "#/components/schemas/OakTown",
                        "description": "Sample class without any special annotations ",
                    }
                ),
            ),
        ),
    ],
)
def test_primitive_to_dict(schema_factory, cls, exp):
    schema = schema_factory.get_schema(cls)
    assert schema.to_dict() == exp
