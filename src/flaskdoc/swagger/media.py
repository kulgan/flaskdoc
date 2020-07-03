import jsonf
from typing import Any

from swagger.models import SwaggerDict


class Content(object):
    def __init__(self):
        super(Content, self).__init__()
        self.contents = SwaggerDict()

    def add_media_type(self, name, media_type):
        self.contents[name] = media_type.dict()

    def dict(self):
        return self.contents


class Sample:

    ghost: int
    spirit: str

    def vido(self):
        return self.spirit


def to_json_schema(obj: Any):
    print(type(obj))


if __name__ == "__main__":
    to_json_schema(1)
    to_json_schema("a")
    to_json_schema(1.2)
