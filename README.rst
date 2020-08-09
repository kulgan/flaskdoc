flaskdoc
========

|PyPi version| |Python version| |ci| |docs| |license| |coverage| |code quality|

FlaskDoc allows developers to programmatically compose openapi specifications for flask endpoints as a part of code
without needing to write a separate yaml file, and it comes with SwaggerUI embedded. Its main focus is on documentation
which frees developers to focus on getting their services coded.

Why flaskdoc
------------

* Focus only on documentation and not introduce some fancy new way of using flask.
* Easily add to existing code without needing to refactor of change the way the code has been written
* Little or no learning curve, as long as a developer is comforatble using flask developers, they can use flaskdoc.
  to learn quickly and not distract So developers focus on writing code
* SwaggerUI integration for quickly testing and iterating through versions
* Automatic data model to JSON Schema transformation that allows for finer grain configuration


Getting Started
---------------
For more detailed documentation visit

Install
"""""""
from pypi

.. code-block::

    $ pip install flaskdoc

from github

.. code-block::

    $ pip install https://github.com/kulgan/flaskdoc/tarball/master

To run examples you will need to install the dev extension

.. code-block::

    $ pip install flaskdoc[dev]

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

* /openapi.yaml
* /openapi.json
* /swagger-ui

Start Documenting
"""""""""""""""""
Now start documenting you flask routes

A simple post example

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

Run your app and visit `/swagger-ui` to see the generated openapi specs

Running Examples
================

Two example projects are currently provided

* `inventory <src/flaskdoc/examples/inventory.py>`_
* `petstore <src/flaskdoc/examples/petstore.py>`_

To run

.. code-block:: bash

    $ pip install flaskdoc[dev]
    $ flaskdoc start -n petstore

Contributing
------------

Don't hesitate to create a `Github issue <https://github.com/kulgan/flaskdoc/issues>`__ for any bugs or suggestions

.. |ci| image:: https://github.com/kulgan/flaskdoc/workflows/ci/badge.svg
    :target: https://github.com/kulgan/flaskdoc/
    :alt: build

.. |PyPi version| image:: https://img.shields.io/pypi/v/flaskdoc.svg
    :target: https://pypi.org/project/flaskdoc/
    :alt: PyPi downloads

.. |Python version| image:: https://img.shields.io/pypi/pyversions/flaskdoc.svg
    :target: https://pypi.org/project/flaskdoc/
    :alt: Python versions

.. |license| image:: https://img.shields.io/pypi/l/flaskdoc.svg
    :target: https://pypi.org/project/flaskdoc/
    :alt: license
.. |docs| image:: https://readthedocs.org/projects/flaskdoc/badge/?version=latest
    :target: https://flaskdoc.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |code quality| image:: https://app.codacy.com/project/badge/Grade/2dafebf021354a42aa62b11d6ab42654
    :target: https://www.codacy.com/manual/kulgan/flaskdoc?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kulgan/flaskdoc&amp;utm_campaign=Badge_Grade
    :alt: Code Quality

.. |coverage| image:: https://app.codacy.com/project/badge/Coverage/2dafebf021354a42aa62b11d6ab42654
    :target: https://www.codacy.com/manual/kulgan/flaskdoc?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kulgan/flaskdoc&amp;utm_campaign=Badge_Coverage
    :alt: Coverage
