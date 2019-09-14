import pytest

import flaskdoc


@pytest.fixture()
def app(request):
    app = flaskdoc.Flask("Test API", version="1.0")
