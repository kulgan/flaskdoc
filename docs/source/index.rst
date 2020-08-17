Welcome to flaskdoc's documentation!
====================================

FlaskDoc is an extension of the puparley know  to programmatically compose openapi specifications for flask endpoints as a part of code
without needing to write a separate yaml file, and it comes with SwaggerUI embedded. Its main focus is on documentation
which frees developers to focus on getting their services coded.

User's Guide
------------
This section provides documentation on how to get started using flaskdoc in your application.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   tutorial
   examples
   snippets
   flaskdoc
   changelog

Quickstart
-----------
Install flaskdoc via ``pip`` or add to your project requirements/dependency

.. code-block::

    $ pip install flaskdoc


Register OpenAPI
""""""""""""""""
Add top level openapi objects like `Info <https://swagger.io/specification/#info-object>`_,
`Contact <https://swagger.io/specification/#contact-object>`_, `License <https://swagger.io/specification/#license-object>`_ etc

.. code-block:: python

    import flask
    from flaskdoc import register_openapi, swagger

    app = flask.Flask()
    # initialize app, add all the blueprints you care about

    # Create top level OpenAPI objects
    # the info object
    info = swagger.Info(
        title="Test",
        version="1.2.2",
        contact=swagger.Contact(
            name="Rowland", email="r.ogwara@gmail.com", url="https://github.com/kulgan"
        ),
        license=swagger.License(name="Apache 2.0", url="https://www.example.com/license"),
    )

    # servers names and variables if necessary
    servers = [swagger.Server(url="http://localhost:15172")]

    # top level tags
    tags = [
        swagger.Tag(name="admin", description="Secured Admin-Only calls"),
        swagger.Tag(name="developers", description="Operations available to regular developers"),
    ]

    security_schemes = {
        "api_key": swagger.ApiKeySecurityScheme(name="api_key"),
    }

    # register spec
    register_openapi(app, info=info, servers=servers, tags=tags, security=security_schemes)

This adds the following endpoints to your list

* /docs
* /docs/openapi.yaml
* /docs/openapi.json

Start Documenting
"""""""""""""""""
Now start documenting you flask routes

.. code-block:: python

    blp = flask.Blueprint("Dummy", __name__, url_prefix="/v1")
    @swagger.POST(
        tags=["administrator"],
        description="Posts an Echo",
        responses={"201": swagger.ResponseObject(description="OK")},
    )
    @blp.route("/echo", methods=["POST"])
    def post():
        req = flask.request.get_json(force=True)
        return flask.jsonify(req), 200

A GET example with path parameter

.. code-block:: python

    blp = flask.Blueprint("Dummy", __name__, url_prefix="/v1")

    @swagger.GET(
        tags=["getEcho"],
        operation_id="getEcho",
        parameters=[swagger.PathParameter(name="sample", schema=str)],
        description="Retrieve echos wit Get",
        responses={
            "200": swagger.ResponseObject(
                description="Success", content=jo.PlainText(schema=jo.Email()),
            )
        },
    )
    @blp.route("/echo/<string:sample>", methods=["GET"])
    def echo(sample: str):
        """
        Sample GET request
        Returns: Echos back whatever was sent

        """
        return sample

Run your app and visit `/docs` to see the generated openapi specs.

Contributing
------------

Don't hesitate to create a `Github issue <https://github.com/kulgan/flaskdoc/issues>`__ for any **bugs** or
**suggestions**.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
