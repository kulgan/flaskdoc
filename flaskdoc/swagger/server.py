from flaskdoc.swagger.core import SwaggerBase, SwaggerDict


class Server(SwaggerBase):
    """ An object representing a Server. """

    def __init__(self, url, description=None):
        super(Server, self).__init__()

        self.url = url
        self.description = description
        self.variables = {}

    def add_variable(self, name, variable):
        """
        Adds a server variable
        Args:
            name (str): variable name
            variable (ServerVariable): Server variable instance
        """
        self.variables[name] = variable.as_dict()

    def __hash__(self):
        return hash((self.url, self.description))

    def __eq__(self, other):
        if not isinstance(other, Server):
            return False
        return self.url == other.url and self.description == other.description


class ServerVariable(SwaggerBase):
    """ An object representing a Server Variable for server URL template substitution. """

    def __init__(self, default_val, enum_values=None, description=None):
        """

        Args:
            default_val (str): REQUIRED. The default value to use for substitution, which SHALL be sent if an alternate
                                value is not supplied. Note this behavior is different than the Schema Object's
                                treatment of default values, because in those cases parameter values are optional.
            enum_values (str|List[str]): An enumeration of string values to be used if the substitution options are
                                from a limited set
            description (str): An optional description for the server variable. CommonMark syntax MAY
                                be used for rich text representation.
        """
        super(ServerVariable, self).__init__()

        enum_values = [enum_values] if isinstance(enum_values, str) else enum_values
        self.default = default_val
        self.enum = enum_values or []
        self.description = description

    def __hash__(self):
        return hash((self.default, self.enum, self.description))

    def __eq__(self, other):
        if not isinstance(other, ServerVariable):
            return False
        return self.default == other.default and self.description == other.description and self.enum == other.enum
