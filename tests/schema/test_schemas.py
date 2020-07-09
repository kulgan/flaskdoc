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
