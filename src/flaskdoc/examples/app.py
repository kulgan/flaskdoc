import flask

import flaskdoc
from flaskdoc.pallets.app import CONFIG


class AppConfig:
    API_LICENSE_NAME = "Apache 2.0"
    API_LICENSE_URL = "https://www.example.com/license"

    API_CONTACT_NAME = "Rowland Ogwara"
    API_CONTACT_EMAIL = "r.ogwara@gmail.com"
    API_CONTACT_URL = "http://www.example.com/rogwa"


def make_app(name="inventory"):
    app = flask.Flask("Test API")

    info = servers = tags = security = None
    if name == "inventory":
        from flaskdoc.examples import inventory

        app.register_blueprint(inventory.blp)
        info = inventory.info
        servers = inventory.servers
        tags = inventory.tags

    elif name == "petstore":
        from flaskdoc.examples import petstore

        app.register_blueprint(petstore.pet)
        app.register_blueprint(petstore.store)
        app.register_blueprint(petstore.user)
        info = petstore.info
        servers = petstore.servers
        tags = petstore.tags
        security = petstore.security_schemes
    elif name == "mocks":
        from flaskdoc.examples import mocks

        app.register_blueprint(mocks.blp)
        info = mocks.info
        tags = mocks.tags
        servers = mocks.servers
    else:
        from flaskdoc.examples import inventory, mocks, petstore

        app.register_blueprint(inventory.blp)
        app.register_blueprint(petstore.pet)
        app.register_blueprint(mocks.blp)
        info = petstore.info
        servers = petstore.servers
        tags = petstore.tags
        security = petstore.security_schemes

    flaskdoc.register_openapi(
        app, info=info, servers=servers, tags=tags, security=security,
    )

    # examples somehow appends an extra docs in the url path, use this force it to empty
    CONFIG["path"] = ""
    return app


def run_examples(example="inventory"):
    app = make_app(name=example)
    app.run(port=80708)
