""" Internal only functions and classes used by both swagger and flask specific customizations """

import collections
import json

import attr

from flaskdoc.pallets import plugins


class DictMixin:
    """General usage mixin for handling nested dictionary conversion."""

    _camel_case_fields_ = False

    def to_dict(self):
        """Converts object to dictionary"""

        return self.parse(self.__dict__)

    def parse(self, val):
        parsed = {}
        convert_to_came_case = val.get("_camel_case_fields_", False)
        for k, v in val.items():
            if k.startswith("__") or k == "_camel_case_fields_":
                # skip private properties
                continue
            # skip None values
            if v is None:
                continue
            if k == "extensions":
                # handle extensions
                extensions = self.parse(v)
                parsed.update(extensions)
                continue
            # map ref
            if k == "ref":
                k = "$ref"
            if k.startswith("_"):
                k = k[1:]
                v = getattr(self, "q_" + k, None)
            k = camel_case(k) if convert_to_came_case else k
            parsed[k] = self._to_dict(v)
        return parsed

    def _to_dict(self, val):
        if isinstance(val, DictMixin):
            return val.to_dict()
        if isinstance(val, list):
            return [self._to_dict(v) for v in val]
        if isinstance(val, collections.Mapping):
            return self.parse(val)
        if hasattr(val, "__dict__"):
            return self.parse(val.__dict__)

        return val


def camel_case(snake_case):
    """Converts snake case strings to camel case

    Args:
        snake_case (str): raw snake case string, eg `sample_text`

    Returns:
        str: camel cased string
    """
    cpnts = snake_case.split("_")
    return cpnts[0] + "".join(x.title() for x in cpnts[1:])


class ApiDecoratorMixin(object):
    """Makes a model a decorator that registers itself"""

    def __call__(self, func):
        plugins.register_spec(func, self)
        return func


@attr.s
class ModelMixin(DictMixin):
    """Swagger Model mixin that provides common methods like to dict and to json"""

    _camel_case_fields_ = attr.ib(default=True, init=False)

    @staticmethod
    def camel_case(snake_case):
        cpnts = snake_case.split("_")
        return cpnts[0] + "".join(x.title() for x in cpnts[1:])

    def json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)

    def convert_props(self, to_camel_case=True):
        self._camel_case_fields_ = to_camel_case


class ExtensionMixin(ModelMixin):

    extensions = attr.ib(default={})

    def add_extension(self, name, value):
        """Allows extensions to the Swagger Schema.

        The field name MUST begin with x-, for example, x-internal-id. The value can be null, a primitive,
        an array or an object.
        Args:
            name (str): custom extension name, must begin with x-
            value (Any): value, can be None, any object or list
        Returns:
            ModelMixin: for chaining
        Raises:
            ValueError: if key name is invalid
        """
        self.validate_extension_name(name)
        if not self.extensions:
            self.extensions = {}
        self.extensions[name] = value
        return self

    @staticmethod
    def validate_extension_name(value):
        """
        Validates a custom extension name
        Args:
            value (str): custom extension name
        Raises:
            ValueError: if key name is invalid
        """
        if value and not value.startswith("x-"):
            raise ValueError("Custom extension must start with x-")

    @extensions.validator
    def validate(self, _, ext):
        """Validates the name of all provided extensions"""
        if ext:
            for k in ext:
                self.validate_extension_name(k)
