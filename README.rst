flaskdoc
========

|PyPi version| |Python version| |ci| |license|

FlaskDoc allows developers to programmatically compose openapi specifications for flask endpoints as a part of code
without needing to write a separate yaml file, and it comes with SwaggerUI embedded. Its main focus is on documentation
which frees developers to focus on getting their services coded.

Why flaskdoc
------------


Getting Started
---------------
Install flaskdoc from pypi

.. code-block::

    $ pip install flaskdoc

To run examples you will need to install the dev extension

.. code-block::

    $ pip install flaskdoc[dev]

Register openapi using flaskdoc, this adds three routes to an existing flask app instance

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
