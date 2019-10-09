import pytest

import flaskdoc

from tests import mocks


class AppConfig(object):
    API_LICENSE_NAME = "Apache 2.0"
    API_LICENSE_URL = "https://www.example.com/license"

    API_CONTACT_NAME = "Rowland Ogwara"
    API_CONTACT_EMAIL = "r.ogwara@gmail.com"
    API_CONTACT_URL = "http://www.example.com/rogwa"


@pytest.fixture(params=[AppConfig])
def app(request):
    _app = flaskdoc.Flask("Test API", version="1.0")
    _app.config.from_object(request.param)
    _app.register_blueprint(mocks.blp, url_prefix="/mocks")

    return _app


if __name__ == '__main__':
    _s_app = flaskdoc.Flask("Test API", version="1.0")
    _s_app.config.from_object(AppConfig)
    _s_app.register_blueprint(mocks.blp, url_prefix="/mocks")

    _s_app.run(port=4444)
