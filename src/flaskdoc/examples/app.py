import flask


class AppConfig:
    API_LICENSE_NAME = "Apache 2.0"
    API_LICENSE_URL = "https://www.example.com/license"

    API_CONTACT_NAME = "Rowland Ogwara"
    API_CONTACT_EMAIL = "r.ogwara@gmail.com"
    API_CONTACT_URL = "http://www.example.com/rogwa"


def make_app():
    app = flask.Flask("Test API")
    # _app.register_blueprint(mocks.blp, url_prefix="/mocks")

    return app
