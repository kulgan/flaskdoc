from flaskdoc.swagger.core import SwaggerBase, SwaggerDict


class Server(SwaggerBase):

    def __init__(self, url, description=None):
        super(Server, self).__init__()
        self.url = url
        self.description = description
        self.variables = {}

    def add_variable(self, name, variable):
        self.variables[name] = variable

    def as_dict(self):
        d = SwaggerDict()
        d["url"] = self.url
        d["description"] = self.description
        if self.variables:
            d["variables"] = {k: v.as_dict() for k, v in self.variables.items()}
        d.update(super(Server, self).as_dict())
        return d

    def __hash__(self):
        return hash((self.url, self.description))

    def __eq__(self, other):
        if not isinstance(other, Server):
            return False
        return self.url == other.url and self.description == other.description


class ServerVariable(SwaggerBase):

    def __init__(self, default_val, enum_values=None, description=None):
        super(ServerVariable, self).__init__()
        self.default = default_val
        self.enums = enum_values or []
        self.description = description

    def as_dict(self):
        d = SwaggerDict()
        d["enum"] = self.enums
        d["default"] = self.default
        d["description"] = self.description

        d.update(super(ServerVariable, self).as_dict())
        return d

    def __hash__(self):
        return hash((self.default, self.enums, self.description))

    def __eq__(self, other):
        if not isinstance(other, ServerVariable):
            return False
        return self.default == other.default and self.description == other.description and self.enums == other.enums
