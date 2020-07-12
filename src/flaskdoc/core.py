import collections
import json

import attr

from flaskdoc.pallets import plugins


class DictMixin:
    """ General usage mixin for handling nested dictionary conversion. """

    def to_dict(self):
        return self._parse_dict(self.__dict__)

    def _parse_dict(self, val: dict):
        parsed = {}
        for k, v in val.items():
            if k == "extensions" or (v not in [True, False] and not v):
                continue
            # map ref
            if k == "ref":
                k = "$ref"
            if k.startswith("_"):
                k = k[1:]
                v = getattr(self, "q_" + k, None)
            parsed[camel_case(k)] = self._to_dict(v)
        return parsed

    def _to_dict(self, val):
        if isinstance(val, DictMixin):
            return val.to_dict()
        if isinstance(val, list):
            return [self._to_dict(v) for v in val]
        if isinstance(val, collections.Mapping) or hasattr(val, "__dict__"):
            return self._parse_dict(val)
        return val


def camel_case(snake_case):
    cpnts = snake_case.split("_")
    return cpnts[0] + "".join(x.title() for x in cpnts[1:])


class ApiDecoratorMixin(object):
    """ Makes a model a decorator that registers itself """

    def __call__(self, func):
        plugins.register_spec(func, self)
        return func


@attr.s
class ModelMixin(DictMixin):
    """ Model mixin that provides common methods like to dict and to json """

    @staticmethod
    def camel_case(snake_case):
        cpnts = snake_case.split("_")
        return cpnts[0] + "".join(x.title() for x in cpnts[1:])

    def json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)

    def __repr__(self):
        return self.json()
