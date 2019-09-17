import collections

from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.parameters import Style


class Content(SwaggerBase):

    def __init__(self):
        self._contents = SwaggerDict()

    def add_media_type(self, name, media_type):
        self._contents[name] = media_type


class MediaType(SwaggerBase):

    def __init__(self):
        super(MediaType, self).__init__()

        self.schema = None
        self.example = None
        self.examples = None
        self.encoding = None


class Encoding(object):

    def __init__(self, content_type, headers=None, style=None, explode=None, allow_reserved=False):

        self.content_type = content_type
        self.headers = headers
        self._style = style if isinstance(style, Style) else Style(style)
        self.explode = explode
        self.allow_reserved = allow_reserved

    def as_dict(self):
        d = SwaggerDict()
        d["contentType"] = self.content_type
        d["headers"] = self.headers
        d["style"] = self._style.value if self._style else None
        d["explode"] = self.explode
        d["allowReserved"] = self.allow_reserved

        return d


class Header(SwaggerBase):

    def __init__(self, required=False,
                 description=None,
                 deprecated=False,
                 allow_empty_value=False,
                 explode=False,
                 allow_reserved=False,
                 schema=None,
                 content=None,
                 example=None,
                 examples=None):

        super(Header, self).__init__()
        self.description = description
        self.deprecated = deprecated

        self.allow_empty_value = allow_empty_value
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = content

        self.explode = explode
        self._required = required
        self._style = Style.SIMPLE
        self.example = example
        self.examples = examples

    @property
    def required(self):
        return self._required

    @property
    def style(self):
        return self._style

    def as_dict(self):
        d = SwaggerDict()
        d["description"] = self.description
        d["required"] = self.required
        d["deprecated"] = self.deprecated
        d["allowEmptyValue"] = self.allow_empty_value
        d["style"] = self.style.value if self.style else None
        d["explode"] = self.explode
        d["allowReserved"] = self.allow_reserved
        d["content"] = self.content.as_dict() if self.content else None
        d.update(super(Header, self).as_dict())
        return d

