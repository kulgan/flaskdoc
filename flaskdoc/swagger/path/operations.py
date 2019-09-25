from flaskdoc.swagger.core import SwaggerBase, SwaggerDict
from flaskdoc.swagger.path import paths


class Operation(SwaggerBase):
    """ Describes a single API operation on a path. """

    def __init__(self, tags=None, summary=None,
                 description=None, operations_id=None):
        super(Operation, self).__init__()
        self.tags = tags or []  # type -> List[str]
        self.summary = summary
        self.description = description
        self.external_docs = None
        self.operation_id = operations_id
        self.parameters = []
        self.request_body = None
        self.responses = None
        self.callbacks = {}
        self.deprecated = False
        self.security = []
        self.servers = set()

    @property
    def http_method(self):
        return None

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    @staticmethod
    def from_op(http_method):
        """
        Factory for creating instances of Http Operations
        Args:
            http_method (str): http method string

        Returns:
            Operation:
        """
        http_method = paths.HttpMethod(http_method)
        if http_method == paths.HttpMethod.GET:
            return GET()
        elif http_method == paths.HttpMethod.POST:
            return POST()
        elif http_method == paths.HttpMethod.PUT:
            return PUT()
        elif http_method == paths.HttpMethod.DELETE:
            return DELETE()
        elif http_method == paths.HttpMethod.OPTIONS:
            return OPTIONS()
        elif http_method == paths.HttpMethod.TRACE:
            return TRACE()
        elif http_method == paths.HttpMethod.PATCH:
            return PATCH()
        elif http_method == paths.HttpMethod.HEAD:
            return HEAD()


class GET(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.GET


class POST(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.POST


class PUT(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.PUT


class HEAD(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.HEAD


class OPTIONS(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.OPTIONS


class PATCH(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.PATCH


class TRACE(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.TRACE


class DELETE(Operation):

    @property
    def http_method(self):
        return paths.HttpMethod.DELETE
