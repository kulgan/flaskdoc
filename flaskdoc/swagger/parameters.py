import collections

from enum import Enum

from swagger import SwaggerBase


class ParameterLocation(Enum):

  COOKIE = "cookie"
  HEADER = "header"
  PATH = "path"
  QUERY = "query"


class Style(Enum):

  FORM = "form"
  LABEL = "label"
  MATRIX = "matrix"
  SIMPLE = "simple"
  SPACE_DELIMITED = "spaceDelimited"
  PIPE_DELIMITED = "pipeDelimited"
  DEEP_OBJECT = "deepObject"


class Parameter(SwaggerBase):

  def __init__(self, name, location,
               required=False,
               description=None,
               deprecated=False,
               style=None,
               allow_empty_value=False,
               explode=False,
               allow_reserved=False,
               schema=None):

    super(Parameter, self).__init__()
    self.name = name
    self.location = location
    self.description = description
    self.deprecated = deprecated

    self.allow_empty_value = allow_empty_value
    self.allowReserved = allow_reserved
    self.schema = schema
    self.content = {}

    self.explode = explode
    self._required = required
    self._style = style

  @property
  def required(self):
    return self._required

  @property
  def style(self):
    return self._style

  def as_dict(self):
    d = collections.OrderedDict(
      name=self.name
    )
    d["in"] = self.location
    d.update(collections.OrderedDict(
      description=self.description,
      required=self.required,
      deprecated=self.deprecated,
      allowEmptyValue=self.allow_empty_value,
      style=self.style,
      explode=self.explode
    ))
    d.update(super(Parameter, self).as_dict())


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
