.. _snippets:

Snippets
========
Code usage examples and snippets


Reusable Components
"""""""""""""""""""
Reusable examples and other components can be adding to the components using:

.. code-block:: python

        from flaskdoc import swagger, register_openapi

        examples = {
            "foo": swagger.Example(value=10)
        }
        links = {
            "l1": swagger.Link(operation_id="L!")
        }

        register_openapi(app, info, examples=examples, links=links)

Reference Objects
"""""""""""""""""
Resuable components can be referenced using proper ReferenceObject

.. literalinclude:: ../../src/flaskdoc/examples/api_with_examples.py
    :language: python
    :linenos:
    :lines: 82-99
    :emphasize-lines: 7, 11

Defining Examples
"""""""""""""""""
.. literalinclude:: ../../src/flaskdoc/examples/api_with_examples.py
    :language: python
    :linenos:
    :lines: 9-60



Using Enums
"""""""""""
.. literalinclude:: ../../src/flaskdoc/examples/link_example/schemas.py
    :language: python
    :linenos:
    :lines: 26-31

.. literalinclude:: ../../src/flaskdoc/examples/link_example/specs.py
    :language: python
    :linenos:
    :lines: 45-59
    :emphasize-lines: 6
