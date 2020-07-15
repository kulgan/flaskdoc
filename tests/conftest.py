import flask
import pytest

import flaskdoc
from flaskdoc import swagger
from tests import mocks


class AppConfig(object):
    API_LICENSE_NAME = "Apache 2.0"
    API_LICENSE_URL = "https://www.example.com/license"

    API_CONTACT_NAME = "Rowland Ogwara"
    API_CONTACT_EMAIL = "r.ogwara@gmail.com"
    API_CONTACT_URL = "http://www.example.com/rogwa"


@pytest.fixture(params=[AppConfig])
def app(request, info_block):
    _app = flask.Flask("Test API")
    _app.register_blueprint(mocks.blp, url_prefix="/mocks")

    get_echo_tag = swagger.Tag(
        name="getEcho", description="gets echos no matter where they are hiding"
    )
    post_echo_tag = swagger.Tag(name="postEcho", description="posts echos to hidden locations")
    flaskdoc.register_openapi(_app, info=info_block, tags=[get_echo_tag, post_echo_tag])
    return _app


@pytest.fixture()
def info_block():
    _info = swagger.Info(
        title="Test",
        version="1.2.2",
        contact=swagger.Contact(
            name="Rowland", email="r.ogwara@gmail.com", url="https://github.com/kulgan"
        ),
        license=swagger.License(name="Apache 2.0", url="https://www.example.com/license"),
    )
    return _info


if __name__ == "__main__":
    _s_app = flask.Flask("Test API")
    _s_app.config.from_object(AppConfig)
    _s_app.register_blueprint(mocks.blp, url_prefix="/mocks")

    flaskdoc.register_openapi(_s_app, info=info_block())
    _s_app.run(port=4444)
