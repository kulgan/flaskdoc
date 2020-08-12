import pytest

from flaskdoc.examples.app import make_app


@pytest.fixture
def app():
    return make_app(name="all")
