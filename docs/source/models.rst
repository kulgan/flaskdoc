.. _jo-data-models:

Data Models
===========

flaskdoc introspects native python objects and converts then into swagger appropriate json schema. Data models can
be defined using either standard python classes, dataclasses or attrs. Flaskdoc will automatically convert them into
json schema.

Generic models
--------------

.. code-block:: python

    from flaskdoc.schema import SchemaFactory

    class OakTown:
    """ Sample class without any special annotations """

        oaks = None
        smugs = 1  # type: int
        snux = "2"  # type: str

    factory = SchemaFactory()
    schema = factory.get_schema(OakTown)
    print(schema.json())
    # {'$ref': '#/components/schemas/OakTown', 'description': 'Sample class without any special annotations '}
    print(factory.schemas['OakTown'])
    # {
    #   "properties": {
    #     "oaks": {
    #       "type": "string"
    #     },
    #     "smugs": {
    #       "type": "integer"
    #     },
    #     "snux": {
    #       "type": "string"
    #     }
    #   },
    #   "type": "object"
    # }

For native python classes like the example above, default values are used to decipher the types, else it defaults to
string. Finer control over types can be achieved using either python data classes or attrs or type annotations

.. code-block:: python

    from typing import List, Set

    @attr.s
    class Sample(object):
        """ Class with mixed attribute definitions """

        danni = "fear"
        palo = attr.ib(type=int)
        soap = attr.ib(type=SoapStar)
        hulu = attr.ib(default="NoNo")

    class Squeezed:
    """ Sample class with typed annotations """

        sample = 1
        spaces = 6


    class SoakedBean(object):

        density: int = None
        samples: List[Sample] = []
        squeezes: Set[Squeezed] = {}

    schema = factory.get_schema(SoakedBean)
    print(schema.json())
    # {"$ref": "#/components/schemas/SoakedBean"}

    print(factory.schemas['SoakedBean'])
    # {
    #  "properties": {
    #    "density": {
    #      "type": "integer",
    #      "format": "int32"
    #    },
    #    "samples": {
    #      "items": {
    #        "$ref": "#/components/schemas/Sample",
    #        "description": "Class with mixed attribute definitions "
    #      },
    #      "type": "array"
    #    },
    #    "squeezes": {
    #      "items": {
    #        "$ref": "#/components/schemas/Squeezed",
    #        "description": "Sample class with typed annotations "
    #      },
    #      "type": "array"
    #    }
    #  },
    #  "type": "object"
    # }

    print(factory.schemas['Sample'])
    # {
    #   "properties": {
    #    "palo": {
    #      "type": "integer",
    #      "format": "int32"
    #    },
    #    "soap": {
    #      "$ref": "#/components/schemas/SoapStar",
    #      "description": "Simple attr based class "
    #    },
    #    "hulu": {
    #      "type": "string"
    #    },
    #    "danni": {
    #      "type": "string"
    #    }
    #  },
    #  "type": "object"
    # }



jo (json objects) models
------------------------

jo is part of flaskdoc builtin functions for defining complex json schema representation from simple/plain/native
python data types. It wraps around `attr` to enable developer provided schema constraints to properties in classes.

-----
.. automodule:: flaskdoc.jo
   :members:
