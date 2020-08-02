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

Define top level objects for you API

Info
----

.. literalinclude:: src.flaskdoc.examples.inventory.py
    :linenos:
    :start-line: 6


Register openapi using flaskdoc, this adds three routes to an existing flask app instance


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
