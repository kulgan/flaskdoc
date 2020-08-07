Examples
========

``flaskdoc`` includes example projects which was used extensively to test the usability of the project. To run examples
``flaskdoc`` needs to be installed as dev using

.. code-block:: bash

    $ pip install flaskdoc[dev]

Running Examples
----------------

Flaskdoc comes with a basic command line tool for running examples that demonstrates the various capabilities of the
project

Usage
#####
flaskdoc examples can be invoked as follows:

.. code-block:: bash

    $ flaskdoc start -n <example>

Where example can either be petstore or inventory, use ``all`` to register all examples at once

Petstore Example
----------------

Implements the standard petstore.swagger.io specification provided by swagger. To run petstore example:

.. code-block:: bash

    $ flaskdoc start -n petstore


Inventory Example
-----------------
Implements the simple inventory api provided by swaggerhub. To run inventory example:

.. code-block:: bash

    $ flaskdoc start -n inventory

Visit http://localhost:{port}/swagger-ui to see the SwaggerUI or http://localhost:{port}/swagger-ui/redoc to see
the redoc version
