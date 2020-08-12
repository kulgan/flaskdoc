""" Internal only functions and classes used by both swagger and flask specific customizations """

import collections
import json

import attr

from flaskdoc.pallets import plugins


class DictMixin:
    """ General usage mixin for handling nested dictionary conversion. """

    _camel_case_fields_ = False

    def to_dict(self):
        """ Converts object to dictionary """

        return self._parse_dict(self.__dict__)

    def _parse_dict(self, val):
        parsed = {}
        # print(val)
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
                extensions = self._parse_dict(v)
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
            return self._parse_dict(val)
        if hasattr(val, "__dict__"):
            return self._parse_dict(val.__dict__)

        return val


def camel_case(snake_case):
    """ Converts snake case strings to camel case

    Args:
        snake_case (str): raw snake case string, eg `sample_text`

    Returns:
        str: camel cased string
    """
    cpnts = snake_case.split("_")
    return cpnts[0] + "".join(x.title() for x in cpnts[1:])


class ApiDecoratorMixin(object):
    """ Makes a model a decorator that registers itself """

    def __call__(self, func):
        plugins.register_spec(func, self)
        return func


@attr.s
class ModelMixin(DictMixin):
    """ Swagger Model mixin that provides common methods like to dict and to json """

    _camel_case_fields_ = attr.ib(default=True, init=False)

    @staticmethod
    def camel_case(snake_case):
        cpnts = snake_case.split("_")
        return cpnts[0] + "".join(x.title() for x in cpnts[1:])

    def json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)

    def convert_props(self, to_camel_case=True):
        self._camel_case_fields_ = to_camel_case
