from enum import Enum

from flaskdoc.swagger.core import SwaggerBase, SwaggerDict


class ParameterLocation(Enum):
    COOKIE = "cookie"
    HEADER = "header"
    PATH = "path"
    QUERY = "query"


class Style(Enum):
    """ Style values defined to aid serializing different simple parameters """

    FORM = "form"
    LABEL = "label"
    MATRIX = "matrix"
    SIMPLE = "simple"
    SPACE_DELIMITED = "spaceDelimited"
    PIPE_DELIMITED = "pipeDelimited"
    DEEP_OBJECT = "deepObject"


class Parameter(SwaggerBase):
    """
    Describes a single operation parameter.
    A unique parameter is defined by a combination of a name and location.
    """

    def __init__(self, name, location="query",
                 required=False,
                 description=None,
                 deprecated=False,
                 style="form",
                 allow_empty_value=False,
                 explode=False,
                 allow_reserved=False,
                 schema=None):
        super(Parameter, self).__init__()
        self.name = name
        self.location = ParameterLocation(location)
        self.description = description
        self.deprecated = deprecated

        self.allow_empty_value = allow_empty_value
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = None

        self.explode = explode
        self._required = required
        self._style = style if isinstance(style, Style) else Style(style)

    @property
    def required(self):
        return self._required

    @property
    def style(self):
        return self._style

    def as_dict(self):
        d = SwaggerDict()
        d["name"] = self.name
        d["in"] = self.location.value if self.location else None

        d["description"] = self.description
        d["required"] = self.required
        d["deprecated"] = self.deprecated
        d["allowEmptyValue"] = self.allow_empty_value
        d["style"] = self.style.value if self.style else None
        d["explode"] = self.explode
        d["allowReserved"] = self.allow_reserved
        d["schema"] = self.schema.as_dict() if self.schema else None
        d["example"] = None
        d["examples"] = {}
        d["content"] = self.content.as_dict() if self.content else None
        d.update(super(Parameter, self).as_dict())
        return d


class PathParameter(Parameter):

    @property
    def required(self):
        return True

    @property
    def style(self):
        return self._style or Style.SIMPLE


class QueryParameter(Parameter):

    @property
    def style(self):
        return self._style or Style.FORM


class HeaderParameter(Parameter):

    @property
    def style(self):
        return self._style or Style.SIMPLE


class CookieParameter(Parameter):

    @property
    def style(self):
        return self._style or Style.FORM


class RequestBody(SwaggerBase):
    """ Describes a single request body. """

    def __init__(self, content, description=None, required=False):
        super(RequestBody, self).__init__()
        self.required = required
        self.description = description
        self.content = content

    def as_dict(self):
        d = SwaggerDict()
        d["description"] = self.description
        d["content"] = self.content.as_dict() if self.content else None
        d["required"] = self.required


if __name__ == '__main__':
    print(ParameterLocation("query"))
