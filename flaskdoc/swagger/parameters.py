from enum import Enum


class ParameterLocation(Enum):

  COOKIE = "cookie"
  HEADER = "header"
  PATH = "path"
  QUERY = "query"


class Style(Enum):

  FORM = "form"
  SIMPLE = "simple"


class Parameter(object):

  def __init__(self, name, location,
               required=False,
               description=None,
               deprecated=False,
               style=None):
    self.name = name
    self.location = location
    self.description = description
    self.deprecated = deprecated

    self._required = required
    self._style = style

  @property
  def required(self):
    return self._required

  @property
  def style(self):
    return self.style


class PathParameter(Parameter):

  @property
  def required(self):
    return True

  @property
  def style(self):
    return self.style or Style.SIMPLE


class QueryParameter(Parameter):

  def style(self):
    return self.style or Style.FORM
