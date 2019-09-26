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

    def __init__(self, name,
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
        self._location = ParameterLocation("query")
        self.description = description
        self.deprecated = deprecated

        self.allow_empty_value = allow_empty_value
        self.allow_reserved = allow_reserved
        self.schema = schema
        self.content = None

        self.explode = explode
        self._required = required
        self._style = style if isinstance(style, Style) else Style(style)

        self.example = None
        self.examples = None

    @property
    def required(self):
        return self._required

    @property
    def style(self):
        return self._style

    @property
    def location(self):
        return self._location.value


class PathParameter(Parameter):

    @property
    def required(self):
        return True

    @property
    def style(self):
        return self._style.value or Style.SIMPLE.value

    @property
    def location(self):
        return ParameterLocation.PATH.value


class QueryParameter(Parameter):

    @property
    def style(self):
        return self._style.valaue or Style.FORM.value


class HeaderParameter(Parameter):

    @property
    def style(self):
        return self._style.value or Style.SIMPLE.value


class CookieParameter(Parameter):

    @property
    def style(self):
        return self._style.value or Style.FORM.value


class RequestBody(SwaggerBase):
    """ Describes a single request body. """

    def __init__(self, content, description=None, required=False):
        super(RequestBody, self).__init__()
        self.required = required
        self.description = description
        self.content = content
