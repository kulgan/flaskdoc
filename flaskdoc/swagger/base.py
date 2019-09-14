import json
from collections import OrderedDict


class SwaggerBase(object):

  def __init__(self):
    self._extensions = None

  def add_extension(self, name, value):
    """
    Allows extensions to the Swagger Schema. The field name MUST begin with x-,
    for example, x-internal-id. The value can be null, a primitive, an array or an object.
    Args:
        name (str): custom extension name, must begin with x-
        value (Any): value, can be None, any object or list
    Returns:
        SwaggerBase: for chaining
    Raises:
        ValueError: if key name is invalid
    """

    self.validate_extension_name(name)

    if not self._extensions:
      self._extensions = OrderedDict()
    self._extensions[name] = value
    return self

  @staticmethod
  def validate_extension_name(name):
    """
    Validates a custom extension name
    Args:
        name (str): custom extension name
    Raises:
        ValueError: if key name is invalid
    """
    if not (name and name.startswith("x-")):
      raise ValueError("Custom extension must start with x-")

  def as_dict(self):
    return OrderedDict(
      extensions=self._extensions
    )

  def __repr__(self):
    return json.dumps(self.as_dict())
