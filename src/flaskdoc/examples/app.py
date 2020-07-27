import flask

import flaskdoc
from flaskdoc import swagger
from flaskdoc.examples import inventory, petstore


class AppConfig:
    API_LICENSE_NAME = "Apache 2.0"
    API_LICENSE_URL = "https://www.example.com/license"

    API_CONTACT_NAME = "Rowland Ogwara"
    API_CONTACT_EMAIL = "r.ogwara@gmail.com"
    API_CONTACT_URL = "http://www.example.com/rogwa"


def make_app(name="inventory"):
    app = flask.Flask("Test API")

    info = inventory.info
    servers = (inventory.servers,)
    tags = inventory.tags
    if name == "inventory":
        app.register_blueprint(inventory.blp)

    elif name == "petstore":
        app.register_blueprint(petstore.pet)
        info = petstore.info
        servers = petstore.servers
        tags = petstore.tags

    flaskdoc.register_openapi(
        app, info=info, servers=servers, tags=tags,
    )
    return app


def run_examples(example="inventory"):
    app = make_app(name=example)
    app.run(port=80708)
