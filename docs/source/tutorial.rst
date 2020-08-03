Getting started
===============
flaskdoc provides decorators that can be used to automatically generate openapi v3 specifications from existing
flask routes. This sections describes how to get started quickly.

Step 1. Install
---------------

``flaskdoc`` is available on `PyPi`_,

.. _PyPi: https://pypi.python.org/pypi/pytest-flask

Step 2. Configure
-----------------
Register flaskdoc with your flask ``app`` instance. This requires top level openapi models like Info, Server, Tags etc.
These should match your api's expectations.
Flaskdoc exposes swagger specific models via ``flaskdoc.swagger`` so

.. code-block:: python

    from flaskdoc import swagger

    contact_info = swagger.Contact(
        name="Contact Name",
        email="Contact Email",
        url="Contact URL",
    )
    license_info = swagger.License(
        name="License Name",
        url="License URL",
    )

    info = swagger.Info(
        title="API title",
        version="API version",
        contact=contact_info,
        license=license_info,
    )

Registering openapi routes using openapi involves simply doing

.. code-block:: python

    import flask
    from flaskdoc import register_openapi, swagger

    app = flask.Flask("Fancy flask App)
    info = swagger.Info(...)

    register_openapi(app, info=info)


Under the hood, flaskdoc simply does a:

.. code-block:: python

    app.add_url_rule("/openapi.json", view_func=register_json_path, methods=["GET"])
    app.add_url_rule("/openapi.yaml", view_func=register_yaml_path, methods=["GET"])
    app.register_blueprint(ui, url_prefix="/swagger-ui")

Step 3. Start Documenting
-------------------------
Again ``flaskdoc`` exposes http method decorators that can be used in documenting your
api via ``flaskdoc.swagger``.

Simple GET
""""""""""
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

Simple POST
"""""""""""
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
