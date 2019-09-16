from swagger import SwaggerBase


class Server(SwaggerBase):

  def __init__(self, url, description=None, variables=None):
    super(Server, self).__init__()
    self.url = url
    self.description = description
    self.variables = variables or {}


class ServerVariable(SwaggerBase):

  def __init__(self, default_val, enum_values=None, description=None):
    super(ServerVariable, self).__init__()
    self.default = default_val
    self.enum = enum_values or []
    self.description = description
