import json

import pytest
from openapi_spec_validator import validate_spec

from flaskdoc.examples.app import make_app


@pytest.fixture
def app():
    return make_app(name="all")


def test_examples_spec_is_valid(client):
    r = client.get("/docs/openapi.json")
    print(json.dumps(r.json, indent=2))
    validate_spec(r.json)
