import flask

import flaskdoc


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
        info = petstore.info
        servers = petstore.servers
        tags = petstore.tags
        security = petstore.security_schemes
    else:
        from flaskdoc.examples import inventory, petstore

        app.register_blueprint(inventory.blp)
        app.register_blueprint(petstore.pet)
        info = petstore.info
        servers = petstore.servers
        tags = petstore.tags
        security = petstore.security_schemes

    flaskdoc.register_openapi(
        app, info=info, servers=servers, tags=tags, security=security,
    )
    return app


def run_examples(example="inventory"):
    app = make_app(name=example)
    app.run(port=80708)
