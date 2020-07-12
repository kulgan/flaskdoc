import flask

import flaskdoc
from flaskdoc import swagger
from flaskdoc.examples import inventory


class AppConfig:
    API_LICENSE_NAME = "Apache 2.0"
    API_LICENSE_URL = "https://www.example.com/license"

    API_CONTACT_NAME = "Rowland Ogwara"
    API_CONTACT_EMAIL = "r.ogwara@gmail.com"
    API_CONTACT_URL = "http://www.example.com/rogwa"


def make_app():
    app = flask.Flask("Test API")
    app.register_blueprint(inventory.blp)

    info = swagger.models.Info(
        title="Test",
        version="1.2.2",
        contact=swagger.Contact(
            name="Rowland", email="r.ogwara@gmail.com", url="https://github.com/kulgan"
        ),
        license=swagger.models.License(name="Apache 2.0", url="https://www.example.com/license"),
    )
    flaskdoc.register_openapi(
        app,
        info=info,
        servers=[swagger.Server(url="http://localhost:15172")],
        tags=[
            swagger.Tag(name="admin", description="Secured Admin-Only calls"),
            swagger.Tag(
                name="developers", description="Operations available to regular developers"
            ),
        ],
    )
    return app


def run_examples():
    app = make_app()
    app.run(port=80708)
